import streamlit as st
from zipfile import ZipFile
from helper import get_people_who_unfollow_me

st.set_page_config(
        page_title='Instagram Unfollow Checker 🔍',
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded",
    )

def main():
    st.sidebar.title("About")
    st.sidebar.info('A simple web app to check who unfollowed you on Instagram.\n\n**How to get your data (<1 min):**\n\nGo to Instagram > Your activity > Download your information > Request a download > Select types of information > Select "Followers and Following" only > Change "Date range" to "All time" > Submit Request\n\nMeta will send you an email once it is ready for download.\n\n**How to use:** \n\nDownload the file, upload it on the right and click Submit.\n\n_Note: You do not have to unzip the file. If you wish to, you may do so and upload only **followers_1.html** and **following.html**._\n\n**Source Code:** https://github.com/zhunhung/instagram_unfollow_checker')

    st.title('Instagram Unfollow Checker 🔍')

    files = st.file_uploader('Upload Files', type=['zip', 'html'], accept_multiple_files=True)
    btn = st.button('Submit')

    if btn:
        filenames = [f.name for f in files]
        if ('following.html') in filenames and ('followers_1.html') in filenames:
            follow = [f for f in files if f.name == 'followers_1.html'][0]
            following = [f for f in files if f.name == 'following.html'][0]
            unfollowers = get_people_who_unfollow_me(follow, following)
            unfollowers = unfollowers.to_html(escape=False)
            st.header('Users who I follow but do not follow me')
            st.write(unfollowers, unsafe_allow_html=True)

        elif (len(filenames) == 1) and (files[0].type == 'application/zip'):
            zip_file = ZipFile(files[0])
            with zip_file.open('connections/followers_and_following/followers_1.html') as follow, zip_file.open('connections/followers_and_following/following.html') as following:   
                unfollowers = get_people_who_unfollow_me(follow, following)
                unfollowers = unfollowers.to_html(escape=False)
                st.header('Users who I follow but do not follow me')
                st.write(unfollowers, unsafe_allow_html=True)

if __name__ == '__main__':
    main()