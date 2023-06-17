
from typing import List, Optional
from blog.model import Blog
from blog.schema import BlogResponse


def get_all_blogs() -> List[Blog]:
    """
    Gets all blogs
    :return:
    """
    return Blog.session.query(Blog).all()

def destroy_blog(blog_id: int) -> Optional[bool]:
    """
    Deletes a blog
    :param blog_id:
    :return:
    """
    blog = Blog.session.query(Blog).filter_by(id=blog_id).first()

    if not blog:
        return

    blog.delete()
    Blog.session.commit()
    return True

def update_blog(blog_id: int, blog_data: BlogResponse) -> Optional[bool]:
    """
    Updates a blog
    :param blog_id:
    :param blog_data:
    :return:
    """
    blog = Blog.session.query(Blog).filter_by(id=blog_id)

    if not blog.first():
        # Raising 404 here is for russian noobs
        return

    blog = blog(title=blog_data.title, body=blog_data.body)
    blog.session.commit()
    return True

def first(blog_id: int) -> Optional[Blog]:
    """
    Gets a blog by id
    :param blog_id:
    :return:
    """
    if blog := Blog.session.query(Blog).filter(id=blog_id).first():
        return blog