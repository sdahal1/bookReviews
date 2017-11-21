from __future__ import unicode_literals

from django.db import models
import re 
import bcrypt 



class UserManager(models.Manager):
    def validateUser(self, post):
        is_valid = True
        errors = []
        if len(post.get('name')) == 0:
            errors.append('Name must not be blank')
        elif len(post.get('name')) < 3:
            errors.append('Name must be at least three characters long')

        user = User.objects.filter(email = post.get('email')).first()
        if user:
            errors.append('This email is already in use.')

        if not re.search(r'\w+\@\w+\.\w+', post.get('email')):
            errors.append('You must enter a valid email format')

        if len(post.get('email')) ==0 :
            errors.append('Email must not be blank')

        if len(post.get('password')) <4:
            errors.append("password must be at least 4 characters")   
        
        if post.get('password') != post.get('confirm_password'):
            errors.append('Your passwords do not match')

        if len(errors)>0:
            is_valid = False
            print errors

        return {'status': is_valid, 'errors': errors} 

    def createUser(self,post):
        return User.objects.create(name = post.get('name'), email = post.get('email'), password = bcrypt.hashpw(post.get('password').encode(), bcrypt.gensalt())
    )

    def deleteall(self):
        User.objects.all().delete()

    def loginUser(self, post):
        user = User.objects.filter(email=post.get('email')).first()
        if user and bcrypt.hashpw(post.get('password').encode(), user.password.encode()) == user.password:
            return {'status': True, 'user': user}
        else:
            return {'status': False, 'message': 'Invalid credentials'}
    
class ReviewManager(models.Manager):
    def validateBookAndReview(self, post):
        is_valid = True
        errors = []
        if len(post.get('title')) == 0:
            errors.append("Book title is required ")
            is_valid = False

        if len(post.get('review')) == 0:
            errors.append("You must submit a review")
            is_valid = False
        
        print post.get('rating')
        if post.get('rating') == "":
            errors.append("your rating is invalid")
            is_valid = False
        elif int(post.get('rating')) < 0 or int(post.get('rating')) > 5:
            errors.append('Your rating must be between 1-5') 

        
        if 'list_author' not in post and len(post.get('new_author'))==0:
            errors.append("You must select an author")
            is_valid = False
        elif 'list_author' in post and len(post.get('new_author')) >0:
            errors.append("Only one author may be selected")
            is_valid= False
        return {'status': is_valid, 'errors': errors}

    def validateReview(self, post):
        is_valid = True
        errors = []
        print post.get('review')
        if len(post.get('review')) == 0:
            errors.append('review must not be blank')
            
        if post.get('rating') == "":
            errors.append("your rating is invalid")
            is_valid = False
        elif int(post.get('rating')) < 1 or int(post.get('rating')) > 5:
            errors.append('Your rating must be between 1-5') 
        return {'status': is_valid, 'errors': errors}
           
            
            


        
    
        

            





class User(models.Model): 
    name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Author(models.Model):
    name = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Book(models.Model): #now we have the author made we can make the book which will call on it that is a foreign key
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name = "books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


#now we make our reviews

class Review(models.Model):
    review = models.TextField()
    rating = models.IntegerField()
    user = models.ForeignKey(User, related_name = "reviews") #the user who is leaving the review and a user has many reviews so the related name should be "reviews"
    book = models.ForeignKey(Book, related_name = "reviews") #the book that the review is for..and a book also has many reviews so reviews in related name aka foreign key
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ReviewManager()



