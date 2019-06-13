from InstagramAPI import InstagramAPI
import random
import os
import glob
import yaml

dirs = ['library']
[os.makedirs(d) for d in dirs if not os.path.exists(d)]

conf = yaml.load(open('config.yml'))
insta_username = conf['instagram']['user']
insta_password = conf['instagram']['password']

# Log in.
instagram_api = InstagramAPI(insta_username, insta_password)
instagram_api.login()


def get_latest_public_followers(username):
    '''Gets the first page of followers for the given user name, filtering out
    any that are private.
    '''
    instagram_api.searchUsername(username)
    user_id = instagram_api.LastJson['user']['pk']
    instagram_api.getUserFollowers(user_id)
    return [user['username'] for user in instagram_api.LastJson['users'] if not user['is_private']]


def get_follower_count(username):
    '''Gets the number of followers for the given user name.
    '''
    instagram_api.searchUsername(username)
    return int(instagram_api.LastJson['user']['follower_count'])


seed_orgs = ['der_greif', 'brownieartphoto', 'lagosphotofestival',
             'latinamericanfotografia', 'aklphotofestival', 'mfonfoto']

random_seed_org = random.sample(seed_orgs, 1)[0]
followers = get_latest_public_followers(random_seed_org)

existing_users = [os.path.split(dir)[-1]
                  for dir in glob.glob('./library/*')]
followers = [f for f in followers if f not in existing_users]
random.shuffle(followers)

print(f"Fetched {len(followers)} followers from {random_seed_org}")

global download_count
download_count = 0

while (download_count + len(existing_users)) < 20:
    random_follower = followers.pop()
    num_followers = get_follower_count(random_follower)

    if num_followers > 1000 or num_followers < 20:
        print(f"{random_follower} had {num_followers} followers; skipping")
    elif random_follower == 'institute_for_luminal_studies':
        print('oops')
    else:
        print(f"Downloading photos of {random_follower}")
        shell_cmd = f"instagram-scraper --media-types=image --profile-metadata --include-location --comments --retry-forever --destination=library --retain-username --maximum=100 {random_follower}"
        os.system(shell_cmd)

        download_count += 1
