import os
import dotenv

# Load environment variable from a .env file
dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import redis
from rq import Connection, Worker

from pepper import hackathon_identity_app, app
from scripts.rename_resumes import FixResumeCommand
from scripts.pending_to_waitlisted import PendingToWaitlistedCommand
from scripts.rename_schools import FixUsersSchoolNames
from scripts.rename_majors import FixUsersMajors
from scripts.print_confirm_email_token import PrintConfirmEmailTokenCommand
from scripts.strip_whitespace_from_special_needs import StripWhitespaceFromSpecialNeedsCommand
from scripts.change_user_status_by_id import ChangeUserStatusByID
from scripts.send_batch_emails import SendPreeventEmailCommand
from scripts.send_recruitment_emails import SendRecruitmentEmailCommand

manager = Manager(hackathon_identity_app)

# Migration commands for when you create DB
Migrate(hackathon_identity_app, app.DB)
manager.add_command('db', MigrateCommand)

# add commands from the scripts directory
manager.add_command('fixresumes', FixResumeCommand)
manager.add_command('pending_to_waitlisted', PendingToWaitlistedCommand)
manager.add_command('fixschools', FixUsersSchoolNames)
manager.add_command('fixmajors', FixUsersMajors)
manager.add_command('print_confirm_email_token', PrintConfirmEmailTokenCommand)
manager.add_command('strip_whitespace_from_special_needs', StripWhitespaceFromSpecialNeedsCommand)
manager.add_command('change_user_status_by_id', ChangeUserStatusByID)
manager.add_command('send_preevent_emails', SendPreeventEmailCommand)
manager.add_command('send_recruitment_emails', SendRecruitmentEmailCommand)


@manager.command
def runworker():
    redis_url = os.getenv('REDIS_URL')
    redis_connection = redis.from_url(redis_url)
    with Connection(redis_connection):
        worker = Worker(['default'])
        worker.work(logging_level=hackathon_identity_app.config['REDIS_LOG_LEVEL'].upper())


@manager.command
def run(port=5000, host='0.0.0.0'):
    hackathon_identity_app.run(port=int(port), host=host)


@manager.shell
def make_shell_context():
    from pepper.teams.models import Team
    from pepper.users.models import User, UserRole
    return dict(app=hackathon_identity_app, DB=app.DB, Team=Team, User=User, UserRole=UserRole)


if __name__ == "__main__":
    manager.run()
