HARDCOVER_PROFILE_QUERY="""
{
  me {
    id
    name
    access_level
    bio
    birthdate
    created_at
    email
    books_count
    membership
    membership_ends_at
    pronoun_personal
    pronoun_possessive
    librarian_roles
    location
    username
    lists {
      slug
      name
      books_count
    }
    followed_lists {
      list {
        slug
        name
      }
    }
  }
}
"""

HARDCOVER_READ_QUERY="""
{
  users(where: {email: {_eq: "damonlbp@hotmail.co.uk"}}) {
    username
    books_count
    name
    user_books {
      book {
        slug
        title
        release_year
        pages
        rating
        description
        book_series {
          series {
            slug
            id
            primary_books_count
            creator {
              name
            }
          }
        }
        activities_count
        image {
          url
        }
        taggings {
          tag {
            tag
          }
        }
      }
      date_added
      last_read_date
      likes_count
      read_count
      review
      review_object
      has_review
    }
    onboarded
  }
}
"""

HARDCOVER_USER_BOOKS_BY_STATUS = """
{
  me {
    user_books {
      user_book_status {
        slug
      }
      book {
        slug
        title
        release_date
        rating
        ratings_count
        pages
        reviews_count
        description
        state
        users_read_count
        created_at
        image {
          url
        }
        book_series {
          series {
            slug
            name
          }
        }
      }
    }
  }
}
"""

SERIES_QUERY = """
{
  series(where: {slug: {_eq: SLUG }}) {
    name
    slug
    description
    author {
      name
      name_personal
    }
    creator {
      username
      membership
    }
    is_completed
    books_count
  }
  book_series(
    where: {series: {slug: {_eq: SLUG }}}
    order_by: {position: asc}
  ) {
    details
    position
    book {
      slug
      default_cover_edition {
        book {
          slug
          title
          release_date
          compilation
        }
        publisher {
          name
        }
        isbn_13
      }
      taggings {
        tag {
          tag
        }
      }
    }
  }
}
"""
