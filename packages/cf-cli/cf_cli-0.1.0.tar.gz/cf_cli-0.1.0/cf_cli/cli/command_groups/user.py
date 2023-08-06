import typer
from pathlib import Path
import orjson

from cf_cli.backend.endpoints.user import get_user_info
from cf_cli.backend.endpoints.token import verify


user = typer.Typer(short_help="This group of commands assist the user with account level operations", no_args_is_help=True)

@user.command("login")
def user_login():
    """
    Logs in the user with an access token they have provided.

    This command prompts the user to enter an access token and then checks if the user is already logged in.
    If the user is already logged in, a prompt is displayed asking if they would like to replace their
    existing access token. The token is verified through the /token/verify endpoint and then cached.
    """
    access_token = typer.prompt(typer.style("Input thy access token which beholds the permissions thee grants Cloudflare CLI 🌍 ", fg="blue"), hide_input=True)
    confirm = typer.confirm(typer.style(f"Are thee willin' to proceed with this here token: {typer.style(f'{access_token[:8]}...', fg='red')} ✅ ", fg="green"))
    if confirm:
        typer.secho(f"Making useth of access token {typer.style(f'{access_token[:8]}...', fg='red')} 😁 ", fg="yellow")
        cache = Path(typer.get_app_dir("Cloudflare CLI")) / ".cache.json"
        with open(cache, 'r') as cache_file:
            if cache_file.read() != "":
                cache_file.seek(0)
                cache_content = orjson.loads(cache_file.read())
            else:
                cache_content = {}
        if not cache_content.get("token", False):
            if verify(access_token)['success']:
                with open(cache, 'wb') as cache_file:
                    cache_content['token'] = access_token
                    cache_file.write(orjson.dumps(dict(cache_content)))
                typer.secho(f"Successfully did check thy token {typer.style(f'{access_token[:8]}...', fg='red')} ✅ ", fg="green")
                typer.secho("Cloudflare CLI bids thee farewell 👋 ", fg="bright_yellow")
            else:
                typer.secho(f"Thy token ({f'{access_token[:8]}...'}) seemeth not to be valid 🚫 ", fg="red")
                raise typer.Exit()
        else:
            tok = cache_content["token"]
            replace = typer.confirm(typer.style(
                f"Wouldst thee liketh to replaceth thy existing token ("
                f"{typer.style(f'{tok[:8]}...', fg='red')}) with "
                f"token {typer.style(f'{access_token[:8]}...', fg='red')}? 🔍 ",
                fg="green"))
            if replace:
                if verify(access_token)['success']:
                    with open(cache, 'wb') as cache_file:
                        cache_content['token'] = access_token
                        cache_file.write(orjson.dumps(dict(cache_content)))
                    typer.secho(f"Successfully did check thy token {typer.style(f'{access_token[:8]}...', fg='red')} ✅ ", fg="green")
                    typer.secho("Cloudflare CLI bids thee farewell 👋 ", fg="bright_yellow")
                else:
                    typer.secho(f"Thy token ({f'{access_token[:8]}...'}) seemeth not to be valid 🚫 ", fg="red")
                    raise typer.Exit()
            else:
                typer.secho("Haply anoth'r day 👋 ", fg="orange")
                raise typer.Exit()
    else:
        typer.secho("Haply anoth'r day 👋 ", fg="bright_yellow")
        raise typer.Exit()

@user.command("info")
def user_info():
    """
    Displays information about the currently logged in user.

    This command will display all the personal data Cloudflare has associated with your account.
    Please note that unless you have set up billing information in Cloudflare, multiple fields such
    as name, country and telephone will be None, as Cloudflare does not have that information.
    """
    info = get_user_info()
    fancy_map = {
        "id_": "👀 Thy ID",
        "email": "✉️  Email proper to thee",
        "first_name": "✨ Thy prime nameth",
        "last_name": "💫 Thine lasteth nameth",
        "username": "🌏 Thee's us'rname",
        "telephone": "📞 Contact number proper to thee",
        "country": "🌍 County of thine residence",
        "zipcode": "🏁 Residency proper to thee",
        "created_on": "🎂 Account seemeth initiated on",
        "modified_on": "📅 Thy account wast altered last on",
        "two_factor_authentication_enabled": "💕 Account proper to thee secur'd with @FA",
        "suspended": "🚫 Thou hast been suspend'd",
        "organizations": "🧑‍🚀 Count of org'nizations thine hast membership",
        "betas": "🙊 Secrets of Cloudflare thine account beholds",
        "has_pro_zones": "🥉 Beholds thee a number of pro zones",
        "has_business_zones": "🥈 Beholds thee a number of business zones",
        "has_enterprise_zones": "🥇 Beholds thee a number of enterprise zones"
    }
    if info:
        typer.secho("Cloudflare hast the following information regarding thee 📚:", fg="green", underline=True)
        user_info = info.dict()
        fancied = user_info
        fancied['created_on'] = f"{user_info['created_on']:%d-%m-%Y %H:%M}"
        fancied['modified_on'] = f"{user_info['modified_on']:%d-%m-%Y %H:%M}"
        fancied['organizations'] = len(user_info['organizations'])
        fixed = {value: fancied[key] for key, value in fancy_map.items()}

        for k, v in fixed.items():
            typer.echo(f"{typer.style(k, fg='yellow')} → {typer.style(v, fg=('cyan' if v else 'red'))}")

@user.command("edit")
def user_edit():
    pass