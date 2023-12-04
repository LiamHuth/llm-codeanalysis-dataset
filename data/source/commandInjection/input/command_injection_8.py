# author: Liam Huth
# December 2023

from jinja2 import Template

def render_template(template_string, user_input):
    complete_template_string = template_string.replace('{{ user_input }}', user_input)
    template = Template(complete_template_string)

    return template.render()

def main():
    user_input = input("Enter your name: ")

    template_string = "Hello {{ user_input }}!"
    
    result = render_template(template_string, user_input)
    print(result)

if __name__ == "__main__":
    main()
