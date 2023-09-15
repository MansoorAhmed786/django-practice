from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, EmailValidator,FileExtensionValidator
from django.core.exceptions import ValidationError

class Book(models.Model):
    # AutoField automatically make increment and mainly use for primary key
    # Primary_key is made
    id = models.AutoField(primary_key=True)
    # Big autofield is same as autofeild but it is used for very large data
    # Big auto field store upto 64 bits
    # id1=models.BigAutoField()
    # # UUID is universal unique identifiers 
    # # It is based on 128 bits and 32 characters hexadecimal code
    # # Unique allows only unique fields
    # uuid = models.UUIDField(unique=True)

    # Char field is used to store characters
    # Editable allow to edit the field
    # error_message allow to customize the error
    title = models.CharField(max_length=200,editable=True)

    # Textfield is same as charfield but it is iunbounded 
    # and doesnot require max_length
    # Textfield for a longer description
    # Null=true allow to store null value
    # unique for date helps to make this column unique with respect to given column(publication_year)
    # same as unique_for_month and for unique_for_year
    # description = models.TextField(null=True,unique_for_date='publication_year')

    # # IntegerField for the publication year
    # # Blank= true allow to leave the field 
    # # db-column allow to specify the database column name
    # # Help text in used for help
    publication_year = models.IntegerField(blank=True,db_column='book_publication' ,help_text='Enter the publication year of the Book.')

    # # DateField for the publication date
    publication_date = models.DateField()

    # # DateTimeField for the date and time the book was added
    # # verbose_name is used for human readability and mostly for documentation
    added_at = models.DateTimeField(auto_now_add=False,verbose_name='Added date')

    # # BooleanField for indicating whether the book is available
    # # Choices allow to give choice
    is_available = models.BooleanField(default=True)#,choices=[('True'),('False')])

    # # FloatField for the average user rating
    # # default fix the default value
    # #Db_index is used to allow weather have to create database index for table for not
    average_rating = models.FloatField(default=0.0,db_index=True,validators=[
                                    MinValueValidator(0.0),
                                    MaxValueValidator(5.0),
                                ])

    # # DecimalField for the price
    # # max_digit allows maximum 10 digits which includes 2 decimal_places(decimal_places)

    # # Custom validator
    def validate_positive(value):
        if value < 0:
            raise ValidationError('Value must be positive.')
    price = models.DecimalField(max_digits=10, decimal_places=2)#,validators=[validate_positive])

    # # URLField for a link to the book's webpage
    book_url = models.URLField()

    # # EmailField for the author's email
    author_email = models.EmailField(validators=[EmailValidator])

    # SlugField for generating slugs from the book title
    slug = models.SlugField(unique=True)

    # FileField for the book cover image
    cover_image = models.ImageField(upload_to='location',validators=[FileExtensionValidator(allowed_extensions=('png','pdf'))])

    # # Filefield stores files
    file = models.FileField(upload_to='location')

    # Filepathfield store path of the file
    file_path = models.FilePathField(path=None)

    # GenericIPAddressField for storing IP addresses
    user_ip = models.GenericIPAddressField()

    # DurationField for the reading time in minutes
    reading_time = models.DurationField()


    # Dunder Methods
    def __str__(self):
        return self.title
    def __lt__ (self, other):
        return self.reading_time < other.reading_time
    def __gt__ (self,other):
        return self.reading_time > other.reading_time
    def __eq__(self,other):
        return self.reading_time==other.reading_time
    
    @classmethod
    def calculate_average_rating(cls):
        return cls.objects.aggregate(models.Avg('average_rating'))
    
    @staticmethod
    def bestseller(average_rating):
        return average_rating >= 4.5


    # ForeignKey to relate to another model (Author in this case)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)

    # Generic foreign key is also like other foriegn keys 
    # and to make one to many releationship
    # but genericForeignKey can be used anywhere in the project
    #  and can make relation with any model class

    # ManyToManyField to relate to multiple genres
    # genres = models.ManyToManyField('Author')
    # OnetoOne releation
    # ant=models.OneToOneField('Author')    

class ProxyBook(Book):
    class Meta:
        proxy = True

    def __str__(self):
        return self.title.upper()


# Author model for the ForeignKey relationship
class Author(models.Model):
    id = models.AutoField( primary_key=True)
    name = models.CharField(max_length=100)
<<<<<<< Updated upstream
=======

    def __str__(self):
        return self.name
>>>>>>> Stashed changes
