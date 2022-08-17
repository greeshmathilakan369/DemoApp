from db_config import get_db_connection





review_query = '''CREATE TABLE public.reviews (
	id serial4 NOT NULL,
	"name" varchar(50) NOT NULL,
	email varchar(50) NOT NULL,
	review text NULL,
	date_added date NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT reviews_pkey PRIMARY KEY (id)

);'''

twitter_query = '''CREATE TABLE public.twitter_data (
	tid int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	"date" varchar(50) NULL,
	username text NULL,
	tweet_text text NULL
);'''


conn = get_db_connection()
cur = conn.cursor()
cur.execute(review_query)
cur.execute(twitter_query)
conn.commit()