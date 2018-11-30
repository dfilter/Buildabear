# below are some of the database tests i made while working on the utls.py file. I kept them incase i needed to test a mthod again.
print Queries.insert_subscription('1', '2')
Queries.insert_user('janed', 'jane.doe@something.com', 'Password#')
Queries.insert_forum_post(2, 'Description for game 2.')
print Queries.select_forum_posts(
    1, hours=8766, order="date_posted", desending=True)
Queries.update_rating(2, rate=1, view=2)
Queries.delete_forum_post(4, 4)
print Queries.select_forum_post(1)
Queries.insert_build(1, 1, "Build Description", "")
print Queries.select_user(username="test")
stats_dict = {
    'luck': 111,
    'faith': 111,
    'intelligence': 111,
    'dexterity': 111,
    'strength': 111,
    'vitality': 111,
    'endurance': 111,
    'attunement': 111,
    'vigor': 111
}
item_list = [
    {'item_id': 1, 'item_name': 'Lothric Knight Stright Sword'}
]
tag_list = [
    {'tag_id': 3, 'tag_name': 'Strength Build'}
]
print DS3Queries.insert_build(
    2, 1, 'stat desc', 'item desc', stats_dict, item_list, tag_list)
print DS3Queries.select_build(1)
DS3Queries.delete_item_relationships(1, item_list)
DS3Queries.delete_tag_relationships(1, tag_list)
DS3Queries.delete_build(2)
DS3Queries.update_stat_allocation(1, stats_dict)
