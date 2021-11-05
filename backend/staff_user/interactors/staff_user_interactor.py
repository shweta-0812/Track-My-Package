from staff_user.repos import staff_user_repo

does_index_exists = staff_user_repo.does_index_exists
create_index = staff_user_repo.create_index
delete_index = staff_user_repo.delete_index
cat_indices = staff_user_repo.cat_indices

get_parcel = staff_user_repo.get_parcel
get_latest_parcel = staff_user_repo.get_latest_parcel
