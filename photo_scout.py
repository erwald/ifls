from instapy import InstaPy, smart_run
import random
import os
import glob
import yaml

dirs = ['library']
[os.makedirs(d) for d in dirs if not os.path.exists(d)]

conf = yaml.load(open('config.yml'))
insta_username = conf['instagram']['user']
insta_password = conf['instagram']['password']

session = InstaPy(username=insta_username,
                  password=insta_password,
                  headless_browser=True,
                  use_firefox=True)

seed_orgs = ['der_greif', 'brownieartphoto', 'lagosphotofestival',
             'latinamericanfotografia', 'aklphotofestival', 'mfonfoto']

with smart_run(session):

    random_seed_org = random.sample(seed_orgs, 1)[0]
    followers = session.grab_followers(
        username=random_seed_org, amount=1000, live_match=False, store_locally=False)

    existing_users = [os.path.split(dir)[-1]
                      for dir in glob.glob('./library/*')]
    followers = [f for f in followers if f not in existing_users]
    random.shuffle(followers)

    print(f"Fetched {len(followers)} followers from {random_seed_org}")

    global download_count
    download_count = 0

    while (download_count + len(existing_users)) < 2:
        random_follower = followers.pop()
        num_followers = len(session.grab_followers(
            username=random_follower, amount=1000, live_match=False, store_locally=False))

        if num_followers > 1000 or num_followers < 20:
            print(f"{random_follower} had {num_followers} followers; skipping")
        else:
            print(f"Downloading photos of {random_follower}")
            shell_cmd = f"instagram-scraper --media-types=image --profile-metadata --include-location --comments --retry-forever --destination=library --retain-username --maximum=100 {random_follower}"
            os.system(shell_cmd)

            download_count += 1
