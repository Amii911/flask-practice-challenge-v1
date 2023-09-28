from config import app, api
from models import Post, Comment
from flask_restful import Resource

# create routes here:

class SortedPost(Resource):
  # sort by title
  def get(self):
    posts = Post.query.sort_by(Post.title).all()
    return (post.to_dict() for post in posts), 200
  

api.add_resource(SortedPost, '/api/sorted_posts')

# Challenge 1
# Create a GET route that goes to /api/sorted_posts. This route should return as json all the posts alphabetized by title.


class PostByAuthor(Resource):
  def get(self, author_name):
    post = Post.query.filter(Post.author == author_name).first()
    return post.to_dict(), 200
  
  
api.add_resource(PostByAuthor, "api/posts_by_author/<author_name>")

# Challenge 2
# Create a GET route that goes to /api/posts_by_author/<author_name>. This route should return as json the post by the author's name. For example: /api/posts_by_author/sara would return all post that belong to sara.

class SearchPost(Resource):
  def get(self, title):
    titles = Post.query.filter(Post.title.ilike(f"%{title}%")).all()

    return [title.to_dict() for title in titles], 200

api.add_resource(SearchPost, "/api/search_posts/<title>")

# Challenge 3
# Create a GET route that goes to /api/search_posts/<title>. This route should return as json all the posts that include the title. Capitalization shouldn't matter. So if you were to use this route like /api/search_posts/frog. It would give back all post that include frog in the title.
# Post.query.filter(Post.title.ilike(f"%{title}%")).all()


class PostOrderedByComments(Resource):
  def get(self):
    postOrders = Post.query.sort_by(len(Post.comments)).desc().all()
    # postOrder = Post.query.sort_by(Post.comments.desc).all()

    return [postOrder.to_dict() for postOrder in postOrders] , 200

api.add_resource(PostOrderedByComments, "/api/posts_ordered_by_comments")
# Challenge 4
# Create a GET route that goes to /api/posts_ordered_by_comments. This route should return as json the posts ordered by how many comments the post contains in descendeding order. So the post with the most comments would show first all the way to the post with the least showing last.

class MostPopularCommenter(Resource):
  def get(self):
    commenter = None
    count = 0
    commenters = [comment.commenter for comment in Comment.query.all()]
    uniq_commenters = list(set(commenters))
    for comment_commenter in uniq_commenters:
      commenter_count = commenters.count(comment_commenter)
      if commenter_count > count:
        commenter = comment_commenter
        count = commenter_count
    return { "commenter": commenter }, 200


# Challenge 5
# Create a GET route that goes to /api/most_popular_commenter. This route should return as json a dictionary like { commenter: "Bob" } of the commenter that's made the most comments. Since commenter isn't a model, think of how you can count the comments that has the same commenter name.
if __name__ == "__main__":
  app.run(port=5555, debug=True)



'''
looking for commenter with the most comments
loop through comments. see which name is repeated 
'''


