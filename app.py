import vobject
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        email = request.form['email']
        phone_number = request.form['phone-number']

        # Create a new vCard object and fill it with the contact information
        card = vobject.vCard()
        card.add('n')
        card.n.value = vobject.vcard.Name(family=last_name, given=first_name)
        card.add('fn')
        card.fn.value = first_name + " " + last_name
        card.add('email')
        card.email.value = email
        card.email.type_param = 'INTERNET'
        card.add('org')
        card.org.value = ['My Project USA']
        card.add('phone')
        card.phone.value = phone_number

        card.prettyPrint()

        # Save the vCard to a file on the server
        filename = last_name + '_Contact.vcf'
        with open(filename, 'w') as f:
            f.write(card.serialize())

        # Generate a publicly accessible URL for the vCard file
        url = request.host_url + filename

        return render_template('result.html', url=url)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
