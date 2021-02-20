from database import db
from sqlalchemy.orm.exc import NoResultFound


def add_to_users(values: dict):

    user = db.Vkuser(
        vk_id=values['vk_id'],
        birthdate=values['birthdate'],
        sex=values['sex'],
        first_name=values['first_name'],
        last_name=values['last_name'],
        city=values['city']
    )

    session = db.Session()
    session.add(user)
    session.commit()


def add_to_blacklist(owner_id, pair_id):

    user = db.Blacklist(owner_id=owner_id, pair_id=pair_id)

    session = db.Session()
    session.add(user)
    session.commit()


def add_to_whitelist(owner_id, pair_id, photos, full_name, url):

    user = db.Whitelist(owner_id=owner_id, pair_id=pair_id, photos=photos, full_name=full_name, url=url)

    session = db.Session()
    session.add(user)
    session.commit()


def remove_from_whitelist(id):

    session = db.Session()
    try:
        user = session.query(db.Whitelist).filter(db.Whitelist.pair_id == id).one()
        add_to_blacklist(user.owner_id, user.pair_id)
        session.delete(user)
        session.commit()
    except NoResultFound:
        pass


def whitelist_ids(user_id):

    session = db.Session()
    query = session.query(db.Whitelist).filter(db.Whitelist.owner_id == user_id).all()
    ids = [row.pair_id for row in query]
    return ids


def blacklist_ids(user_id):

    session = db.Session()
    query = session.query(db.Blacklist).filter(db.Blacklist.owner_id == user_id).all()
    ids = [row.pair_id for row in query]
    return ids


def check_id_in_database(id):

    session = db.Session()
    query = session.query(db.Vkuser).filter(db.Vkuser.vk_id == id).all()
    ids = [row.vk_id for row in query]
    return int(id) in ids


def show_whitelist(id):

    session = db.Session()
    query = session.query(db.Whitelist).filter(db.Whitelist.owner_id == id).all()
    return [[row.pair_id, row.full_name, row.photos, row.url] for row in query]


def marked_ids(user_id):

    return blacklist_ids(user_id) + whitelist_ids(user_id)


def user_info(user_id):

    info = dict()
    session = db.Session()
    query = session.query(db.Vkuser).filter(db.Vkuser.vk_id == user_id).one()
    info['vk_id'] = query.vk_id
    info['birthdate'] = query.birthdate
    info['sex'] = query.sex
    info['first_name'] = query.first_name
    info['last_name'] = query.last_name
    info['city'] = query.city

    return info


def drop_blacklist(user_id):

    session = db.Session()
    query = session.query(db.Blacklist).filter(db.Blacklist.owner_id == user_id)
    for obj in query:
        session.delete(obj)
    session.commit()


def drop_whitelist(user_id):

    session = db.Session()
    query = session.query(db.Whitelist).filter(db.Whitelist.owner_id == user_id)
    for obj in query:
        session.delete(obj)
    session.commit()


def delete_user(user_id):

    session = db.Session()
    query = session.query(db.Vkuser).filter(db.Vkuser.vk_id == user_id)
    for obj in query:
        session.delete(obj)
    session.commit()
