from flask import render_template
from flask_login import login_required, current_user

from .. import account
from ..forms import AddressForm
from oasis_nourish.models import Address
from oasis_nourish import db

@account.route("/address", methods=["GET", "POST"])
@login_required
def address():
    form = AddressForm()
    if form.validate_on_submit():
        new_address = Address(
            street=form.street.data,
            suburb=form.suburb.data,
            city=form.city.data,
            postal_code=form.postal_code.data,
            user_id=current_user.id
        )
        db.session.add(new_address)
        db.session.commit()

    addr = Address.query.filter_by(user_id=current_user.id).first()
    mode = "add" if addr is None else "view"

    return render_template("account/address.html", mode=mode, address_form=form, address=addr)
