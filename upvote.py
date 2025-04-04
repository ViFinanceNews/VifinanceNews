import flask
import os
import redis

app = flask.Flask(__name__)
UP_VOTE=1
DOWN_VOTE=-1

# Initialize Redis client
r = redis.Redis(
  host='usable-racer-46648.upstash.io',
  port=6379,
  password=os.getenv('REDIS_STR'),
  ssl=True
)

@app.route('/vote', methods=['POST'])
def upvote():
    data = flask.request.get_json()
    url = data.get('url')
    vote_type = data.get('vote_type')

    try:
        # Update Redis cache
        redis_key = f"article:{url}"
        current_vote_type = r.hget(redis_key, "vote_type")
        current_vote_type = int(current_vote_type) if current_vote_type else 0  # Default to 0 if not set

        if vote_type == UP_VOTE:
            if current_vote_type == 1:
                # Undo upvote
                r.hincrby(redis_key, "upvote", -1)
                r.hset(redis_key, "vote_type", 0)
            elif current_vote_type == -1:
                # Change downvote to upvote
                r.hincrby(redis_key, "upvote", 2)
                r.hset(redis_key, "vote_type", 1)
            else:
                # Add upvote
                r.hincrby(redis_key, "upvote", 1)
                r.hset(redis_key, "vote_type", 1)

        elif vote_type == DOWN_VOTE:
            if current_vote_type == -1:
                # Undo downvote
                r.hincrby(redis_key, "upvote", 1)
                r.hset(redis_key, "vote_type", 0)
            elif current_vote_type == 1:
                # Change upvote to downvote
                r.hincrby(redis_key, "upvote", -2)
                r.hset(redis_key, "vote_type", -1)
            else:
                # Add downvote
                r.hincrby(redis_key, "upvote", -1)
                r.hset(redis_key, "vote_type", -1)

        return flask.jsonify({'status': 'success'})
    except Exception as e:
        return flask.jsonify({'status': 'error', 'message': str(e)})