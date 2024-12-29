from django.shortcuts import render ,HttpResponseRedirect , redirect , get_object_or_404
from .forms import signupform ,UserLoginForm ,PostForm
from django.contrib.auth import authenticate , login , logout
from django.contrib  import messages
from .models import post
# Create your views here.
def home(request):
    posts = post.objects.all()
    return render(request , "blog/home.html" , {"posts" : posts})

def about(request):
    return render(request,"blog/about.html")

def dashboard(request):
    if request.user.is_authenticated:
        posts = post.objects.all()
        return render(request , "blog/dashboard.html" , {"posts" : posts})
    else:
        return HttpResponseRedirect("/login/")



def contact(request):
    return render(request , "blog/contact.html")

    
def user_signup(request):
    if request.method == "POST":
        fm = signupform(request.POST)
        if fm.is_valid():
            fm.save()
            messages.success(request ," hurray! you registerd!!")
    else:
        fm = signupform()
    return render(request , "blog/signup.html" , {"form" : fm})

# def user_signup(request):
#     if request.method == "POST":
#         fm = signupform(request.POST)
#         if fm.is_valid():
#             fm.save()  # Save the form data to the database
#               # Redirect to a 'home' page or another success page
#     else:
#         fm = signupform()  # Render an empty form for GET request

#     # Render the form for both invalid POST and GET requests
#     return render(request, "blog/signup.html", {"form": fm})

def user_login(request):
    if request.user.is_authenticated:
        # If the user is already authenticated, redirect to the dashboard or another page
        return redirect('/dashboard/')

    if request.method == "POST":
        fm = UserLoginForm(request=request, data=request.POST)
        if fm.is_valid():
            # Extract cleaned data from the form
            uname = fm.cleaned_data["username"]
            upass = fm.cleaned_data["password"]

            # Authenticate the user
            user = authenticate(username=uname, password=upass)
            if user is not None:
                # Successful login
                login(request, user)
                messages.success(request, "Welcome! You are now logged in.")
                return redirect('/dashboard/')
            else:
                # Authentication failed
                messages.error(request, "Invalid username or password.")
        else:
            # Form is not valid
            messages.error(request, "Please correct the errors below.")

    else:
        # GET request, show the empty login form
        fm = UserLoginForm()

    return render(request, "blog/login.html", {"form": fm})
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def updatepost(request, id):
    if request.user.is_authenticated:
        # Fetch the post or return 404 if not found
        
        if request.method == "POST":
            # Populate the form with the POST data and the post instance
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()  # Save the updated post
                return redirect("/dashboard/")
        else:
            # Render the form pre-filled with the post data for GET request
            form = PostForm(instance=post)
        
        # Render the template with the form
        return render(request, "blog/updatepost.html", {"form": form})
    else:
        return redirect("/login/")
    
def addpost(request):
    if request.user.is_authenticated:  # Check if the user is authenticated
        if request.method == "POST":
            form = PostForm(request.POST)  # Bind the form with POST data
            if form.is_valid():
                # Save the post only if the form is valid
                post = post(
                    title=form.cleaned_data["title"],
                    description=form.cleaned_data["description"],
                    author=request.user  # Assuming the Post model has an author field
                )
                post.save()
                return redirect("/dashboard/")  # Redirect to the dashboard
        else:
            # Handle GET request by rendering an empty form
            form = PostForm()

        # Render the form for both GET requests and invalid POST submissions
        return render(request, "blog/addpost.html", {"form": form })
    else:
        # Redirect unauthenticated users to the dashboard or login page
        return HttpResponseRedirect("/login/")


def deletepost(request, id):
    if request.user.is_authenticated:
        # Get the post object or return 404 if it doesn't exist
  # Restrict deletion to the author
        if request.method == "POST":
            post.delete()  # Delete the post
            return redirect("/dashboard/")  # Redirect after successful deletion
        else:
            # Handle non-POST requests gracefully (e.g., display confirmation page)
            return render(request, "blog/delete.html", {"post": post})
    else:
        # Redirect unauthenticated users to the login page
        return redirect("/login/")

    
def user_profile(request):
    return render(request , "blog/profile.html")
    

