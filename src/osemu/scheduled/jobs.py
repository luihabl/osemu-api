from osemu.extensions import scheduler
from osemu.api import models

def fetch_github_data():
    
    from osemu.extensions import db
    from osemu.api.views.base_views import get_or_create_obj
    from osemu.api import schema
    from github import Github
    from datetime import datetime
    import os
    
    db.create_all()

    token = os.environ.get('GITHUB_TOKEN', None)
    if token:
        gh = Github(os.getenv('GITHUB_TOKEN'))
    else:
        print('No APIToken available.')
        exit(1)

    emulators : list[models.Emulator] = db.session.query(models.Emulator).all()
    for emu in emulators:
        gh_url = emu.git_url
        
        if not gh_url or gh_url == '':
            print(f'No git url defined.')
            continue

        print(f'Updating data of {emu.name} @ {gh_url}')

        if gh_url.endswith('/'):
            gh_url = gh_url.rstrip('/')
            emu.git_url = gh_url
        
        id = '/'.join(gh_url.split('/')[-2:])
        repo = gh.get_repo(id)

        emu.gh_stars = repo.stargazers_count
        emu.gh_forks = repo.forks_count

        latest_commit = repo.get_commits()[0]
        emu.latest_update = datetime.strptime(latest_commit.last_modified, '%a, %d %b %Y %H:%M:%S %Z')
        emu.release_date = repo.created_at

        languages = []
        langs = repo.get_languages()
        for lang_name, lang_amount in langs.items():

            lang_obj = db.session.query(models.Language).filter_by(name=lang_name).first()
            if not lang_obj:
                lang_obj = models.Language(name=lang_name)
                emu_lang = models.EmulatorLanguage(language=lang_obj, emulator=emu, amount=lang_amount)
            else:
                emu_lang = db.session.query(models.EmulatorLanguage).filter_by(language=lang_obj, emulator=emu).first()
                if not emu_lang:
                    emu_lang = models.EmulatorLanguage(language=lang_obj, emulator=emu, amount=lang_amount)
                else:
                    emu_lang.amount = lang_amount

            languages.append(emu_lang)

        emu.language_amounts = languages

        license = None
        try:
            license = repo.get_license()
        except:
            print(f'No license found for {emu.name}')
            emu.license = None
        
        if license:
            name = license.license.name

            try:
                url = license.license.html_url
            except:
                url = ''

            if name == 'Other':
                name = f'{emu.name} License'
                url = license.html_url

            lic_obj = db.session.query(models.License).filter_by(name=name).first()

            if not lic_obj:
                lic_obj = models.License(name=name, url=url)
            
            lic_obj.url = url
            
            emu.license = lic_obj

        emu.short_description = repo.description

        if repo.homepage:
            emu.website_url = repo.homepage

    try:
        db.session.commit()
    except:
        db.session.rollback()
        print('Failed to save data')

 
@scheduler.task('interval', id='fetch_gh_data_1', hours=12, misfire_grace_time=900)
def fetch_gh_data():

    print('Fetching Github data')

    with scheduler.app.app_context():
    
        try:
            fetch_github_data()
            print('Data fetching finished.')
        except Exception as e:
            print('Failed to fetch Github data:')
            print(e)

        
    