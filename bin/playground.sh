#! /bin/bash

# # Here is a comment
# # Permissions: chmod 740 bin/playground.sh
# chmod user:group:other
# echo 'hello world'

# # Capital = system variables
# echo our shell name is $BASH
# echo $BASH_VERSION
# # Lowercase = user variables
# name=Mark
# echo The name is $name

# # Receive input
# echo Enter your name:
# read name
# echo Your name is $name
# echo 'Your name is $name'
# echo "Your name is $name"  # ...  Double quotes interpolate single do not

# echo Hi $name what are your 3 favorite numbers?
# read num1 num2 num3
# echo "$num1, $num2, $num3 are my favorite too!"

# read -p 'Favorite sport?: ' sport
# echo "$sport you say... hmm"

# read -sp 'Favorite secret? ' secret
# echo "$secret!!!"

# echo Hi $name what are your 3 favorite animals?
# read -a animals
# echo "Hmm ${animals[2]}, ${animals[0]}, ${animals[1]}"

# # Pass arguments
# echo arg 0: $0 arg 1: $A arg: 2 $2 end here
# # 0th arg is script name, 'A' wont register

# blah=("$@") # args
# # Will only give first arg unless broken up
# echo all my ${blah[0]} ${blah[1]} are here!  # No index out of range it seems

# # Conditionals
# read -p 'What is the count? ' count
# if [ $count -eq 10 ]  # == for string comparison, whitespace between brackets matters...
# then
#     echo 'The count is 10'
# elif [ $count -gt 10 ]
# then
#     echo 'The count is greater than 10'
# else
#     echo 'The count is less than 10'
# fi

# # Finding files
# read -p 'What is the name of the file you are looking for?: ' file_name
# if [ -e $file_name ]  # -e if the file_name exists
# then
#     echo 'The file was found'
# else
#     echo 'The file was not found'
# fi

# # Logical AND OR operator
# read -p 'What is your age: ' age
# if [ $age -gt 18 ] && [ $age -lt 30 ]  # or [ $age -gt 18 -a $age -lt 30 ]
# then
#     echo 'Age is valid'
# else
#     echo 'Age is invalid'
# fi

# read -p 'What is your favorite number: ' num
# if [ $num -eq 18 ] || [ $num -eq 30 ]
# then
#     echo 'Favorite number is valid'
# else
#     echo 'Favorite number is invalid'
# fi

# # Case
# read -p 'What is the best color on the American flag? ' color
# case $color in
#     'red') echo 'Red is a nice color';;
#     'white') echo 'White is a great choice';;
#     'blue') echo 'Blue is very blue';;
#     *) echo "$color is not on the flag"
# esac

# # Functions
# function hello() {
#     echo 'Hello'
# }

# goodbye() {
#     echo 'Goodbye'
# }
# # 2 ways same result
# hello
# goodbye
