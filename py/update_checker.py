import subprocess
import requests
import os

# The API URL for the latest commit on your dev branch
GITHUB_API_URL = "https://api.github.com/repos/GeovaneJefferson/timemachine/commits/dev"
# URL for release metadata (used when showing notes to user)
GITHUB_RELEASE_URL = "https://api.github.com/repos/GeovaneJefferson/timemachine/releases/latest"

def get_local_commit():
    """Gets the ID of the code currently on your machine.

    Returns None if the folder is not a git repository or the command fails.
    """
    try:
        # Get the folder where this script lives to run git in the right spot
        repo_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if not os.path.isdir(os.path.join(repo_path, '.git')):
            # not a git repo
            return None
        return subprocess.check_output(
            ['git', 'rev-parse', 'HEAD'], 
            cwd=repo_path, 
            stderr=subprocess.STDOUT
        ).decode('utf-8').strip()
    except Exception:
        return None

def get_update_info():
    current_sha = get_local_commit()
    
    try:
        # Ask GitHub for the newest commit ID
        response = requests.get(GITHUB_API_URL, timeout=10)
        response.raise_for_status()
        latest_sha = response.json().get('sha')

        if not latest_sha:
            return {'success': False, 'error': 'Could not find latest commit on GitHub'}

        # if we don't have a local commit we probably aren't in a git repo
        if current_sha is None:
            return {'success': False, 'error': 'Local installation is not a git repository; automatic updates are unavailable'}

        # Compare IDs
        update_available = (latest_sha != current_sha)

        result = {
            'success': True,
            'update_available': update_available,
            'current_version': current_sha[:7] if current_sha else "Unknown",
            'latest_version': latest_sha[:7],
            # We keep these keys so about.js doesn't break
            'release_url': "https://github.com/GeovaneJefferson/timemachine"
        }

        # if there's an update available, try to fetch release notes
        if update_available:
            try:
                rel_resp = requests.get(GITHUB_RELEASE_URL, timeout=10)
                rel_resp.raise_for_status()
                result['release_notes'] = rel_resp.json().get('body', '')
            except Exception:
                result['release_notes'] = ''

        return result
    except Exception as e:
        return {'success': False, 'error': str(e)}

if __name__ == "__main__":
    print(get_update_info())
def perform_update():
    """Pull the latest code from the dev branch and return the output.
    This is intentionally simple; more sophisticated installers would be
    required for packaged apps.
    """
    repo_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # verify git repository
    if not os.path.isdir(os.path.join(repo_path, '.git')):
        return {'success': False, 'error': 'Not a git repository; cannot perform update'}
    try:
        output = subprocess.check_output(['git', 'pull', 'origin', 'dev'], cwd=repo_path,
                                         stderr=subprocess.STDOUT)
        return {'success': True, 'output': output.decode('utf-8', errors='ignore')}
    except subprocess.CalledProcessError as e:
        return {'success': False, 'error': e.output.decode('utf-8', errors='ignore')}
    except Exception as e:
        return {'success': False, 'error': str(e)}
