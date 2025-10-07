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

SEARCH_SERIES = """
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

FOLLOWED_PROMPTS = """
{
  me {
    followed_prompts {
      prompt {
        answers_count
        books_count
        created_at
        description
        question
        prompt_books {
          answers_count
          book {
            slug
            title
            rating
            ratings_count
            release_date
            reviews_count
            description
            taggings_aggregate {
              nodes {
                tag {
                  tag_category {
                    category
                  }
                  tag
                }
              }
            }
          }
        }
      }
    }
  }
}

"""

SEARCH_PROMPT = """
{
  prompts(where: {slug: {_eq: SLUG }}) {
    answers_count
    books_count
    created_at
    description
    question
    prompt_books {
      answers_count
      book {
        slug
        title
        rating
        ratings_count
        release_date
        reviews_count
        image {
          url
        }
        description
        book_series {
          series {
            slug
            name
          }
        }
        taggings {
          tag {
            tag_category {
              id
              tags {
                tag
              }
            }
          }
        }
      }
    }
  }
}
"""

FOLLOWED_LISTS = """
{
  me {
    lists {
      slug
      list_books {
        position
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
          description
          book_series {
            series {
              slug
              name
            }
          }
          taggings {
            tag {
              tag
            }
          }
        }
      }
    }
  }
}
"""

SEARCH_LISTS = """
{
  lists(where: {slug: {_eq: SLUG }}) {
    slug
    name
    followers_count
    description
    created_at
    books_count
    list_books {
      position
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
        description
        book_series {
          series {
            slug
            name
          }
        }
        taggings {
          tag {
            tag
          }
        }
      }
    }
  }
}
"""
