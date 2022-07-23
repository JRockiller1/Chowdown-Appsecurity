
from locale import currency
from flask_mail import Mail
from flask import Flask, flash, render_template, render_template_string, url_for, request, session
from werkzeug.utils import redirect,secure_filename
from sqlalchemy import and_
from app import app, db
from app.models import Customer, Restadmin, Items, Orders, Rating,Promotion,charity_vote
import datetime
import random
from flask_mail import Mail,Message
import os
import bcrypt
import stripe
import imgbbpy
import aiohttp
import asyncio

# password for chowdownfeedback054@gmail.com: chowdownadmin123
# maill pass zswcovyhpabvtnrs
# put in os environ variable

YOUR_DOMAIN = 'http://localhost:5000'

# stripe_keys = {
#     "secret_key": 'sk_test_51L7ztQFZRxIbs7Knrfzv2kk0AKxdl3Zdu5HAnHGbDE5gZq3cN4FJhlFARnyCXT3F1D1TiXQztF992q7pxz17F4Vk00qV2QyIEb',
#     "publishable_key": 'pk_test_51L7ztQFZRxIbs7KnKj6cvm0iOLnojpA8zmi2xeC3D3Zxd9a2vDsEASKpRs9w9HWIRlWYhv9c70N07Ee55FYgYDWa00lV6QS5Yv',
# }
stripe.api_key = 'sk_test_51L7ztQFZRxIbs7Knrfzv2kk0AKxdl3Zdu5HAnHGbDE5gZq3cN4FJhlFARnyCXT3F1D1TiXQztF992q7pxz17F4Vk00qV2QyIEb'
app.config.update(dict(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'chowdownfeedback054@gmail.com',
    MAIL_PASSWORD = 'zswcovyhpabvtnrs'
))
mail = Mail(app)


# UPLOAD_FOLDER = 'app/static/images/product_image'
UPLOAD_FOLDER = '/Users/gabri/appsec/appdev_final_8JUNE/Chowdown-Appsecurity/app/static/images/product_image'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/index')
@app.route("/")
def landingPage():
    # # if logged in to an account
    # # 1st of every month popup form on landing page when they visit the website
    # currentDate = datetime.datetime.now()
    # month = currentDate.month
    # orgs2 = charity_vote.query.filter(charity_vote.month==month).all()
    # minds = 0
    # spca = 0
    # scs = 0
    # for i in orgs2:
    #     if i.organisation == "MINDS":
    #         minds += 1
    #     elif i.organisation == "SPCA":
    #         spca += 1
    #     elif i.organisation == "SCS":
    #         scs += 1
    # organisations = ["MINDS", "SPCA", "SCS"]
    # charity = [minds,spca,scs]
    # chosen=organisations[charity.index(max(charity))]
    # print(chosen)
    return render_template('landingPage.html', restadmin=Restadmin.query.all())

@app.errorhandler(404)
def error_404(e):
    return render_template("Errorpage.html")

@app.route('/indexmenu', methods = ['GET','POST'])
def indexmenu():
    if request.method == "GET":
        restid = request.args.get("restid")
    
    elif request.method == "POST":
        restid = request.form['restid']

    items = Items.query.filter(Items.rid == restid).all()
    restad = Restadmin.query.filter(Restadmin.rid == restid).first()
    return render_template('indexmenu.html',restad=restad, restadmin=items)



# RESTRAUNT/VENDOR
@app.route('/restSignup', methods = ['GET','POST'])
def restlogin():
    return render_template('signup-vendor.html')

@app.route('/restSignup-next', methods = ['GET','POST'])
def restregisterbyadmin():	
    if request.method == "GET":
        rmail = request.args.get("rmail")
        rmobile = request.args.get("rmobile")

    elif request.method == "POST":
        rmail = request.form['rmail']
        rmobile = request.form['rmobile']
        rpassword = request.form['rpassword']
        rname = request.form['rname']
        raddress = request.form['raddress']
        # r = Vendor(rname,raddress,rmail,rpassword,rmobile)
        restadmin = Restadmin.query.filter(and_(Restadmin.rmail == rmail, Restadmin.rmobile == rmobile)).first()
        salt = bcrypt.gensalt(rounds=14)
        pwhash = bcrypt.hashpw(rpassword.encode(),salt)

        if restadmin:
            # return redirect(url_for('adminHome1'))		
            return render_template('signup-vendor.html', admsg="Restaurant Already Registered...!")
        # add in alert to say restraunt is registered already
        else:
            newrest = Restadmin(rname=rname, rmail=rmail, rmobile=rmobile, raddress=raddress, rpassword=pwhash)
        
            db.session.add(newrest)
            db.session.commit()

            return render_template('login-vendor.html')
            # return render_template('vendorProfile.html', ssmsg="Restaurant Registered Succcessfully...!")

@app.route('/restLogin')
def restLogin():
    return render_template("login-vendor.html")

@app.route('/restLogin-next',methods=['GET','POST'])
def restloginNext():
    # To find out the method of request, use 'request.method'

    if request.method == "GET":
        rmail = request.args.get("rmail")
        rpassword = request.args.get("rpassword")
    
    elif request.method == "POST":
        rmail = request.form['rmail']
        rpassword = request.form['rpassword']

       
        restadmin  = Restadmin.query.filter(Restadmin.rmail == rmail).first()
        pw_storedhash = restadmin.rpassword


        # if restadmin and rpassword.isnumeric():
        #     session['rmail'] = request.form['rmail']
        #     return redirect(url_for('resthome1'))
        if restadmin and bcrypt.checkpw(rpassword.encode(),pw_storedhash) :
            session['rmail'] = request.form['rmail']
            return redirect(url_for('resthome1'))
            # return render_template('resthome.html',rusname=restadmin.rname,restadmin = Restadmin.query.all())
            # return render_template('resthome.html',restadmin = Restadmin.query.all())
            
       
        return render_template('login-vendor.html',rusname="Login failed...\n Please enter valid username and password!")

@app.route('/restprofile')
def restProfile():
    if not session.get('rmail'):
        return redirect(request.url_root)
    rmail=session['rmail']

    restadmin=Restadmin.query.filter(Restadmin.rmail==rmail).first()

    return render_template('vendorProfile.html',restname=restadmin.rname, restinfo = restadmin)

@app.route('/editrestprofile')
def editrestProfile():
    if not session.get('rmail'):
        return redirect(request.url_root)
    rmail=session['rmail']
    restadmin=Restadmin.query.filter(Restadmin.rmail==rmail).first()

    return render_template('editvendorprofile.html',restname=restadmin.rname, restinfo = restadmin)

@app.route('/changepassrest')
def changepassrest():
    if not session.get('rmail'):
        return redirect(request.url_root)
    rmail = session['rmail']
    restadmin=Restadmin.query.filter(Restadmin.rmail==rmail).first()

    return render_template('changepassrest.html', info=restadmin)

@app.route('/changepassrestnext', methods=['POST','GET'])
def changepassrestnext():
    if request.method == 'POST':

        rmail = request.form['mail1']
        rpassword = request.form['password1']
    elif request.method == "GET":
        rmail = request.args.get("mail1")
        rpassword = request.args.get("password1")


    restadmin=Restadmin.query.filter(Restadmin.rmail==rmail).first()
    pw_storedhash = restadmin.rpassword
    if restadmin and bcrypt.checkpw(rpassword.encode(),pw_storedhash):
            return render_template('changepassrestnext.html')
    else:
        restadmin=Restadmin.query.filter(Restadmin.rmail==rmail).first()
        return render_template('changepassrest.html', info=restadmin,cmsg="Invalid password entered")
@app.route('/updatepasswordrest',methods=['POST','GET'])
def updatepasswordrest():
    if request.method == 'POST':
        rpassword = request.form['rpassword']
        rpassword2 = request.form['rpassword2']
    elif request.method == "GET":

        rpassword = request.args.get("rpassword")
        rpassword2 = request.args.get("rpassword2")
    
    if rpassword == rpassword2:
        rmail=session['rmail']
        restadmin=Restadmin.query.filter(Restadmin.rmail==rmail).first()
        salt = bcrypt.gensalt(rounds=14)
        pwhash = bcrypt.hashpw(rpassword.encode(),salt)
        restadmin.rpassword=pwhash
        db.session.commit()
        return render_template('changepassrestnext.html',cmsg1="Sucessfully updated password")
    else:
        return render_template('changepassrestnext.html',cmsg2="Passwords do not match")


@app.route('/editrestprofileNext', methods = ['GET','POST'])
def editrestprofileNext():
    if not session.get('rmail'):
        return redirect(request.url_root)
    rmail=session['rmail']
    ruser_name = request.form["rname"]
    remail_address = request.form["remail"]
    raddress = request.form["raddress"]
    rmobile = request.form["rmobile"]
    rpassword = request.form['rpassword']
    rid = request.form['rid']
    restadmin =Restadmin.query.filter(Restadmin.rid==rid).first()
    restadmin.rmail = remail_address
    restadmin.rname = ruser_name
    restadmin.rmobile = rmobile
    restadmin.raddress = raddress
    restadmin.rpassword = rpassword
    db.session.commit()
    flash("Successfully updated profile")
    return render_template('vendorProfile.html', cmsg="Passsword Updated Succcessfully...!", restinfo = restadmin)
@app.route('/resthome1',methods=['GET','POST'])
def resthome1():
    if not session.get('rmail'):
        return redirect(request.url_root)
    rmail=session['rmail']
    restadmin  = Restadmin.query.filter(Restadmin.rmail == rmail).first()
    rid=restadmin.rid
    items = Items.query.filter(Items.rid == rid).all()
    # myorders = Orders.query.filter(Orders.rid == rid)
    myorders = Orders.query.filter(Orders.rid == rid)
    return render_template('resthome.html',rusname=restadmin.rname,restadmin = Restadmin.query.all(), items=items)

@app.route("/restMenu", methods=["GET","POST"])
def menu1():
    if not session.get('cmail'):
        return redirect(request.url_root)

    if request.method == "GET":
        restid = request.args.get("restid")

    elif request.method == "POST":
        restid = request.form['restid']

    items = Items.query.filter(Items.rid == restid).all()
    restad = Restadmin.query.filter(Restadmin.rid == restid).first()
    rating = Rating.query.filter(Rating.rid==restid).all()
    # restad1 = Restadmin.query.filter(Restadmin.rid == restid).all()
    return render_template('restMenu.html',restad=restad, restadmin=items, rating=rating)	

#
@app.route("/restdashboard", methods= ["POST","GET"])
def restdashboard():
    if not session.get('rmail'):
        return redirect(request.url_root)
    rmail=session['rmail']
    restad  = Restadmin.query.filter(Restadmin.rmail == rmail).first()
    restid=restad.rid

    currentDate = datetime.datetime.now()
    month = currentDate.month

    orders = Orders.query.filter(Orders.rid == restid).all()
    jan,feb,mar,apr,may,jun,jul,aug,sep,oct,nov,dec = 0,0,0,0,0,0,0,0,0,0,0,0
    for m in orders:
        if m.month1 == 1:
            jan += m.tprice
            print(jan)
        if m.month1 == 2:
            feb += m.tprice
            print(feb)
        if m.month1 == 3:
            mar += m.tprice
            print(mar)
        if m.month1 == 4:
            apr += m.tprice
            print(apr)
        if m.month1 == 5:
            may += m.tprice
            print(may)
        if m.month1 == 6:
            jun += m.tprice
            print(jun)
        if m.month1 == 7:
            jul += m.tprice
            print(jul)
        if m.month1 == 8:
            aug += m.tprice
            print(aug)
        if m.month1 == 9:
            sep += m.tprice
            print(sep)
        if m.month1 == 10:
            oct += m.tprice
            print(oct)
        if m.month1 == 11:
            nov += m.tprice
            print(nov)
        if m.month1 == 12:
            dec += m.tprice
            print(dec)

    totalprice = 0
    for p in orders:
        totalprice += p.tprice

    totalprice_lastmonth = 0
    orders_lastmonth = Orders.query.filter(Orders.month1 == month-1).all()
    


    
    # previous month revenue
    
    # (current month revenue - previous month revenue) / previous month revenuye * 100
    user=[]
    for i in orders:
       if i.cid not in user:
         user.append(i.cid)
    uuser=len(user)
    print(jan)
    month2=[jan,feb,mar,apr,may,jun,jul,aug,sep,oct,nov,dec]
    month3=["January","February","March","April","May","June","July","Augest","September","October","November","December"]
    products = []
    for o in orders:
        products.append(o.items)
    torders=[]
    for i in range(len(products)):
        if "," in products[i]:
            temporder=products[i].split(',')
            for w in range(len(temporder)):
                torders.append(temporder[w])
        else:
            torders.append(products[i])
    def most_frequent(List):
        counter = 0
        num = List[0]
        for i in List:
            curr_frequency = List.count(i)
            if (curr_frequency > counter):
                counter = curr_frequency
                num = i
        return num
    mostfrequent=most_frequent(torders)
    monthly=month2[month-1]
    
    monthly2=month3[month-1]
    items = Items.query.filter(Items.iid == mostfrequent).all()
    
    for name in items:
        mostfrequent = name.iname

    return render_template("restdashboard.html", orders=orders,
    jan=round(jan,2),feb=round(feb,2), 
    mar=round(mar,2),apr=round(apr,2),
    may=round(may,2),jun=round(jun,2),
    jul=round(jul,2),aug=round(aug,2),
    sep=round(sep,2),oct=round(oct,2),
    nov=round(nov,2),dec=round(dec,2),
    tprice=round(totalprice,2),
    uuser=uuser,monthly=round(monthly,2),
    monthly2=monthly2,
    most_frequent=mostfrequent)


@app.route("/add-product", methods=["POST","GET"])
def add():
    if not session.get('rmail'):
        return redirect(request.url_root)
    return render_template('add-product.html')

@app.route("/add-product-next", methods=["POST","GET"])
def additemNext():
    if not session.get('rmail'):
        return redirect(request.url_root)
    if request.method == "GET":
        iname = request.args.get("iname")
        iprice = request.args.get("iprice")
        idescription = request.args.get("idesc")
    
    elif request.method == "POST":
       
        iname = request.form['iname']
        iprice = request.form['iprice']
        idescription = request.form["idesc"]
        file = request.files['ipic']
    
    rmail=session['rmail']
    restad  = Restadmin.query.filter(Restadmin.rmail == rmail).first()
    restid=restad.rid
    items = Items(iname=iname, iprice=iprice, rid=restid, idesc=idescription,priceid="temp")
    db.session.add(items)
    db.session.commit()
    iid = items.iid

    
    filename = secure_filename(file.filename)
    # mimetype = pic.mimetype
 
 
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    elif file and allowed_file(file.filename):
            
        file.filename = str(iid) + ".png"
            
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
   
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
       
        client = imgbbpy.SyncClient('d92793a1e6a23ddf9b758139fce4a106')
        image = client.upload(file='/Users/gabri/appsec/appdev_final_8JUNE/Chowdown-Appsecurity/app/static/images/product_image/' + filename)
        print(image.url)
        product = stripe.Product.create(
            name=iname,
            id = iid,
            images = [image.url])
        price = stripe.Price.create(
            product=product.id,
            unit_amount = round((float(iprice)*100)),
            currency='sgd')
        items = Items.query.filter(Items.iid==iid).first()
        items.priceid = price.id
        db.session.commit()
    return redirect(url_for('resthome1'))
    # except:

    #     if file.filename == '':
    #         flash('No image selected for uploading')
    #         return redirect(request.url)
    #     if file and allowed_file(file.filename):
        
    #         file.filename = str(iid) + ".png"
        
    #         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))    
            
    #         return redirect(url_for('resthome1'))

# @app.route("/edit-product")
# def edit():
#     return render_template("edit-product.html")

@app.route('/updateitem',methods = ['GET','POST'])
def updateitem():
    if not session.get('rmail'):
        return redirect(request.url_root)
    return render_template('edit-product.html')


@app.route('/updateitemNext',methods = ['GET','POST'])
def updateitemNext():
    if not session.get('rmail'):
        return redirect(request.url_root)
    if request.method == "GET":
        iid = request.args.get("iid")
        iname = request.args.get("iname")
        iprice = request.args.get("iprice")
        idesc = request.args.get("idesc")
        file = request.args.get("ipic")
    elif request.method == "POST":
        iid = request.form['iid']
        iname = request.form['iname']
        iprice = request.form['iprice']
        idesc = request.form['idesc']
        file = request.files['ipic']
        # iname = request.form['iname']
        # iprice = request.form['iprice']
        # p = Product(None,None)
        # p.set_price(request.form['iprice'])
        # p.set_name(request.form['iname'])
        
    rmail=session['rmail']
    restad  = Restadmin.query.filter(Restadmin.rmail == rmail).first()
    restid=restad.rid

    item = Items.query.filter(and_(Items.iid ==iid,Items.rid==restid)).first()
    if item :
        if len(iname) > 0:
            item.iname= iname
        if iprice != "":
            item.iprice = iprice
        if idesc != "":
            item.idesc = idesc
        if file.filename != "":
             if file and allowed_file(file.filename):
                file.filename = str(iid) +".png"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        db.session.commit()
        # add new price
        price = stripe.Price.create(
            product = item.iid,
            unit_amount = round((float(iprice)*100)),
            currency='sgd'
        )
        print(iname)
        print(item.iid)
        # change name.
        stripe.Product.modify(
            item.iid,
            name = iname
        )
        # add new price to db
        item.priceid = price.id 
        db.session.commit()

        return redirect(url_for('resthome1'))
    else :
        # return redirect(url_for('updateitem'))		
        return render_template('updateitem.html',imsg="Error! Item id does not belong to you..! ")



@app.route('/deleteitem',methods = ['GET','POST'])
def deleteitem():
    if not session.get('rmail'):
        return redirect(request.url_root)
    return render_template('removeitem.html')	


@app.route('/deleteitemNext',methods = ['GET','POST'])
def deleteitemNext():
    if not session.get('rmail'):
        return redirect(request.url_root)
    if request.method == "GET":
        iid = request.args.get("iid")
    
    elif request.method == "POST":
        iid = request.form['iid']
    
    rmail=session['rmail']
    restad  = Restadmin.query.filter(Restadmin.rmail == rmail).first()
    restid=restad.rid

   
    item = Items.query.filter(and_(Items.iid ==iid,Items.rid==restid)).first()
    if item :          
        db.session.delete(item)
        db.session.commit()
        return redirect(url_for('resthome1'))
    else:
        errorcode = "Product ID is invalid. Please enter again"
        return render_template('removeitem.html',imsg="Error! Item id does not belong to you..! ",errorcode=errorcode)

@app.route("/createpromo")
def createpromo():
    return render_template("promocode.html")

@app.route("/createpromonext", methods=["GET","POST"])
def createpromonext():
    if request.method == "GET":
        promocode = request.args.get('promocode')
        discount = request.args.get('discount')
    elif request.method == "POST":
        promocode = request.form['promocode']
        discount = request.form['discount']
        duration = request.form['duration']
    # create coupon, assign promocode to coupon
    coupon = stripe.Coupon.create(
        percent_off=discount,
        duration="repeating",
        duration_in_months = duration,
        )
    stripe.PromotionCode.create(
        code=promocode,
        coupon=coupon
    )

    rmail=session['rmail']
    restad  = Restadmin.query.filter(Restadmin.rmail == rmail).first()
    restid=restad.rid
    promotion = Promotion(rid=restid, promocode=promocode, discount=discount)
    db.session.add(promotion)
    db.session.commit()
    return redirect(url_for('resthome1'))

@app.route('/create-checkout-session',methods=['POST','GET'])
def create_checkout_session():
    if request.method == "GET":
        # tprice = request.args.get("total")
        items = request.args.get("items")
        rid=request.args.get("restid")
        
    
    elif request.method == "POST":
        tprice=request.form['total']
        items=request.form["items"]
        rid=request.form['restid']

    restadmin  = Restadmin.query.filter(Restadmin.rid == rid).first()
    # items = Items.query.filter(Items.rid == restid, Items.iname==restname).all()
    rname=restadmin.rname
    cmail=session['cmail']
    customer  = Customer.query.filter(Customer.cmail == cmail).first()

    line_items = []
    quantity = 0
    for i in items.split(','):
        item2 = Items.query.filter(Items.iid == i).first()
        # get price and quantity based on item id. one by one
        
        print(items.split(',').count(i))
        if items.split(',').count(i)>1:
            quantity = items.split(',').count(i)
            priceid = item2.priceid
            a = {
                'price':priceid,
                # need to get price id instead of actual price
                'quantity':quantity
            }
            line_items.append(a)
            break
            
        # do if loop if same item but > 1 item
        else:
            priceid = item2.priceid
            a = {
                'price':priceid,
                'quantity':1
            }
            line_items.append(a)
        # append to line items for stipe checkout
    print(line_items)

    # try:
    checkout_session = stripe.checkout.Session.create(
        line_items=line_items,
        mode='payment',
        allow_promotion_codes= True,
        success_url= YOUR_DOMAIN + '/success.html',
        cancel_url= YOUR_DOMAIN + '/cancel.html',
        )
    currentDate = datetime.datetime.now()
    #change to show how month work for graph
    month = currentDate.month
    paymentType = "DELETE THIS ATTRIBuTEstr"
    cid = customer.cid
    orders = Orders(cid=customer.cid, rid=rid, items=items,tprice=tprice,payment=paymentType,month1=month,rname=rname)
    
      

    
    if orders :
        db.session.add(orders)
        db.session.commit()

    return redirect(checkout_session.url,code=303)






# @app.route('/cart', methods = ['GET','POST'])
# def payment():
#     if not session.get('cmail'):
#         return redirect(request.url_root)
#     if request.method == "GET":
#         tprice = request.args.get("total")
#         items = request.args.get("items")
#         rid=request.args.get("restid")
        
    
#     elif request.method == "POST":
#         tprice=request.form['total']
#         items=request.form["items"]
#         rid=request.form['restid']
#     print("========================================= items")
#     print(items)

    

#     #//////////////////////////////////////////////////////////////////////////////////////// 
#     if(tprice=="0"):
#     # return (str(tprice=="0"))
#         return render_template('errorzero.html')	
#         # return redirect(url_for('restmenu'))
#         #////////////////////////////////////////////////////////////////////////////////////

#     cmail=session['cmail']
#     customer  = Customer.query.filter(Customer.cmail == cmail).first()
#     cid = customer.cid
#     promo = Promotion.query.filter(Promotion.rid==rid).all()
#     # for i in promo:
#     #     print (i.promocode)
#     item = Items.query.filter(Items.iid == items)
#     item2 = Items.query.filter(Items.iid == items)
    


#     restadmin  = Restadmin.query.filter(Restadmin.rid == rid).first()
#     # items = Items.query.filter(Items.rid == restid, Items.iname==restname).all()

#     rname=restadmin.rname
#     myorders = Orders.query.filter(Orders.cid == cid).all()
#     print(myorders)
#     totalprice = 0
#     for i in myorders:
#         totalprice += i.tprice
#     print(totalprice)
#     if totalprice >= 0:
#         tier = "IRON"
#         discount = 0
#     if totalprice > 100:
#         tier = "BRONZE"
#         discount = 1
#     if totalprice > 500:
#         tier = "SILVER"
#         discount = 2
#     if totalprice > 2000:
#         tier = "GOLD"
#         discount = 5
#     if totalprice > 10000:
#         tier = "PLATNIUM"
#         discount = 8
#     # items = Items.query.filter()
#     # iname = restadmin.iname
#     ostatus="pending"
#     subtotal = float(tprice)
#     tprice = round(float(tprice),2)
#     if discount == 0:
#         pass
#     else:
#         tprice -= float(tprice)*(float(discount)/100)
#     x={temp:items.count(temp) for temp in items}
#     try:
#         c=","
#         x.pop(c)
#         print(items)
#         return render_template('cart.html' ,x=x, tprice=tprice, rname=rname ,items=items, rid=rid,promo=promo,tier=tier,discount=discount,subtotal=subtotal)
#     except:
#         print(items)
#         return render_template('cart.html' ,x=x,tprice=tprice, rname=rname ,items=items, rid=rid,promo=promo,tier=tier,discount=discount,subtotal=subtotal)

# @app.route("/discountedcart")
# def discountedcart():
#     if not session.get('cmail'):
#         return redirect(request.url_root)
#     if request.method == "GET":
#         tprice = request.args.get("tprice")
#         items = request.args.get("items")
#         rid=request.args.get("restid")
#         promocode = request.args.get("promocode")
#         subtotal = request.args.get("subtotal")
    
#     elif request.method == "POST":
#         tprice=request.form['tprice']
#         items=request.form["items"]
#         rid=request.form['restid']
#         promocode = request.form["promocode"]
#         subtotal = request.form["subtotal"]
#     print(items)
#     print(tprice)
#     #//////////////////////////////////////////////////////////////////////////////////////// 
#     if(tprice=="0"):
#     # return (str(tprice=="0"))
#         return render_template('errorzero.html')	
#         # return redirect(url_for('restmenu'))
#         #////////////////////////////////////////////////////////////////////////////////////

#     cmail=session['cmail']
#     customer  = Customer.query.filter(Customer.cmail == cmail).first()
#     cid = customer.cid
#     promo = Promotion.query.filter(Promotion.rid==rid).all()
#     promocode1 = ""
#     for i in promo:
#         if promocode == i.promocode:
#             tprice = float(tprice)
#             print(i.discount)
#             discount = (i.discount/100)*tprice
#             dprice = tprice - discount
#             discountpercent = i.discount
#             # round(tprice,2)
#             # print(tprice)
            

#     restadmin  = Restadmin.query.filter(Restadmin.rid == rid).first()
#     # items = Items.query.filter(Items.rid == restid, Items.iname==restname).all()

#     rname=restadmin.rname

#     # items = Items.query.filter()
#     # iname = restadmin.iname
#     ostatus="pending"
#     totalprice = 0
#     myorders = Orders.query.filter(Orders.cid == cid).all()

#     for i in myorders:
#         totalprice += i.tprice
#     if totalprice >= 0:
#         tier = "IRON"
#         discount1 = 0
#     if totalprice > 100:
#         tier = "BRONZE"
#         discount1 = 1
#     if totalprice > 500:
#         tier = "SILVER"
#         discount1 = 2
#     if totalprice > 2000:
#         tier = "GOLD"
#         discount1 = 5
#     if totalprice > 10000:
#         tier = "PLATNIUM"
#         discount1 = 8
#     x={temp:items.count(temp) for temp in items}
#     # if discount1 == 0:
#     #     pass
#     # else:
#     #     tprice = t float(tprice)*(float(discount1/100))

#     # tprice = round((dprice - totalprice),2)
#     print("ACTUAL TOTAL PRICE BOZO TO BE SOTRED IN DATABASE")
#     print(dprice)
#     try:
#         c=","
#         x.pop(c)

#         return render_template('cart_afterdiscount.html' ,x=x, tprice=tprice, dprice=round(dprice,2),rname=rname ,items=items, rid=rid,promo=promo,promocode=promocode,tier=tier,discount1=discount1,subtotal=subtotal,discountpercent=discountpercent)
#     except:
  
#         return render_template('cart_afterdiscount.html' ,x=x, tprice=tprice, dprice=round(dprice,2),rname=rname ,items=items, rid=rid,promo=promo,promocode=promocode,tier=tier,discount1=discount1,subtotal=subtotal,discountpercent =discountpercent)




# @app.route('/updaterestpass',methods = ['GET','POST'])
# def updaterestprofile():
#     if not session.get('rmail'):
#         return redirect(request.url_root)
#     return render_template('updaterestpass.html')


# @app.route('/updaterestpassNext', methods = ['GET','POST'])
# def updaterestprofileNext():
#     if not session.get('rmail'):
#         return redirect(request.url_root)
    
#     rmail=session['rmail']
#     r = Vendor(None,None,None,None,None)
#     r.set_pass( request.form['rpassword'])
#     # rpassword = request.form['rpassword']
    
#     restadmin=Restadmin.query.filter(Restadmin.rmail==rmail).first()
#     # restadmin.rpassword=rpassword
#     restadmin.rpassword = r.get_password()
#     db.session.commit()
#     return render_template('updaterestpass.html', rmsg="Passsword Updated Succcessfully...!")

@app.route('/restprofile', methods = ['GET','POST'])
def showrestprofile():
    if not session.get('rmail'):
        return redirect(request.url_root)
    
    rmail=session['rmail']

    restadmin=Restadmin.query.filter(Restadmin.rmail==rmail).first()
    # customer.cpassword=cpassword
    # db.session.commit()
    return render_template('vendorProfile.html',resinfo = restadmin)

@app.route('/forgorpasswordrest',methods=["POST","GET"])
def forgorpasswordrest():
    if request.method == "GET":
        rmail = request.args.get("rmail")

    
    elif request.method == "POST":
        rmail = request.form['rmail']


        
    new_pass = random.randint(100,999)

    return render_template('forgorpasswordrest.html',temppass=new_pass)

@app.route('/forgorNextrest', methods = ['GET','POST'])
def forgorpasswordNextrest():
    if request.method == "GET":
        temppass = request.args.get("temp")
        remail = request.args.get('rmail')
    
    elif request.method == "POST":
        temppass = request.form['temp']
   
        remail = request.form["rmail"]

    restadmin=Restadmin.query.filter(Restadmin.rmail==remail).first()
    rmail = restadmin.rmail
        # send pin to email
    msg = Message("Hello from Chow Down! Here is your pin to access your account.", sender="chowdownadmin054@gmail.com", recipients=[rmail])
    msg.body = "Your Pin: " + str(temppass)
    mail.send(msg)
    db.session.commit()
    session['rmail'] = rmail
    return render_template('forgorpasswordNextrest.html',temppass=temppass,restinfo = restadmin)

@app.route('/verifyrest', methods=['POST','GET'])
def verifyrest():
    if request.method == "GET":
        temppass = request.args.get("temp")
        pin = request.args.get("pin")
    
    elif request.method == "POST":
        temppass = request.form['temp']
        pin = request.form['pin']

    if temppass == pin:
        return render_template("changepassrestnext.html")
    else:
        return render_template("forgorpasswordNextrest.html",cmsg="Pin is incorrect. Please try again")
# =====================================================================================================================
# CUSTOMERS
# =====================================================================================================================
@app.route("/sign-in", methods=["POST","GET"])
def signin():
    return render_template('signup.html')

@app.route('/sign-up-successful',methods=['GET','POST'])
def success():
    if request.method == "GET":
        cmail = request.args.get("cmail")
        cpassword= request.args.get("cpassword")
        cname = request.args.get("cname")
        caddress = request.args.get("caddress")
        cmobile= request.args.get("cmobile")
    

    elif request.method == "POST":
        cmail = request.form["cmail"]
        cpassword = request.form["cpassword"]
        cname = request.form["cname"]
        cmobile= request.form["cmobile"]
        caddress = request.form["caddress"]
    
        customercheck = Customer.query.filter(Customer.cmail == cmail).first()
        
        # return(str(customer))
        if customercheck:
            return render_template('signup.html',cmsg="Registration Falied, \n User Already Registered..!")
        else:
            # password hash (BAD)
            # pwhash = sha256(cpassword.encode('utf8'))
            # customer = Customer(cname=cname,cmail=cmail,cmobile=cmobile, caddress=caddress, cpassword=pwhash.hexdigest())
            # ==========================================================================================
            # password hash with salting and pbdfk2 (good) OR BCRYPT
            # pbkdf2 better for encryption (key derivation. Their purpose is to generate an encryption key given a password. )
            # BCYRPT for password storage, much longer/harder to bruteforce (slow hashing).

            salt = bcrypt.gensalt(rounds=14)
            pwhash = bcrypt.hashpw(cpassword.encode(),salt)
            
            
            customer = Customer(cname=cname,cmail=cmail,cmobile=cmobile, caddress=caddress, cpassword=pwhash)
            db.session.add(customer)
            db.session.commit()
            return render_template('login.html')


@app.route('/feedback',methods=['GET','POST'])
def feedback():
    if request.method == "GET":
        fmail = request.args.get("email")
        name = request.args.get("name")
    
    elif request.method == "POST":
        fmail = request.form['email']
        name = request.form['name']
        subject = request.form['subject']
        message = request.form['message']

    msg = Message("Hello from Chow Down!", sender="chowdownadmin054@gmail.com",recipients=[fmail])
    msg2 = Message("Customer Feedback/Enquiry", sender="chowdownadmin054@gmail.com", recipients=["chowdownadmin054@gmail.com"])
    msg.body = "Greetings " + name + "! We have received your enquiry and will get back to you as soon as possible!"
    msg2.body = "From: " + fmail + "\n" + "Subject: " + subject + "\n" + "Message: " + message
    mail.send(msg)
    mail.send(msg2)
    return render_template("landingPage.html")


@app.route('/newsletter', methods=['GET','POST'])
def newsletter():
    if request.method == "GET":
        nmail=request.args.get("nmail")
    elif request.method == "POST":
        nmail = request.form['nmail']

    msg = Message("Hello from Chow Down!", sender="chowdownadmin054@gmail.com",recipients=[nmail])
    msg.body = "Greetings! You are now subscribed to our newsletter!"
    mail.send(msg)
    return url_for("landingPage")


@app.route('/feedback-logged',methods=['GET','POST'])
def feedbacklogged():
    if request.method == "GET":
        fmail = request.args.get("email")
        name = request.args.get("name")
    
    elif request.method == "POST":
        fmail = request.form['email']
        name = request.form['name']
    

    msg = Message("Hello from Chow Down!", sender="chowdownadmin054@gmail.com",recipients=[fmail])
    msg.body = "Greetings " + name + "! We have received your enquiry and will get back to you as soon as possible!"
    mail.send(msg)
    return render_template("loggedinlanding.html")


@app.route('/newsletter-logged', methods=['GET','POST'])
def newsletterlogged():
    if request.method == "GET":
        nmail=request.args.get("nmail")
    elif request.method == "POST":
        nmail = request.form['nmail']
    msg = Message("Hello from Chow Down!", sender="chowdownadmin054@gmail.com",recipients=[nmail])
    msg.body = "Greetings! You are now subscribed to our newsletter!"
    mail.send(msg)
    return render_template("loggedinlanding.html")


@app.route('/login', methods=["POST","GET"])
def login():
    return render_template('login.html')

@app.route('/login-success', methods=['GET','POST'])
def loginsuccess():
    # if not session.get('cmail'):
    #     return redirect(request.url_root)
    if request.method == "GET":
        cmail = request.args.get("cmail")
        cpassword = request.args.get("cpassword")
    
    elif request.method == "POST":
        cmail = request.form['cmail']
        cpassword = request.form['cpassword']
  
        customer  = Customer.query.filter(Customer.cmail == cmail).first()
        pw_storedhash = customer.cpassword
    
        # if customer and cpassword.isnumeric():
        #     session['cmail'] = request.form['cmail']
        #     return redirect(url_for('userLanding'))

        if customer and bcrypt.checkpw(cpassword.encode(),pw_storedhash):
            session['cmail'] = request.form['cmail']
            return redirect(url_for('userLanding'))
        # return render_template('loggedinLanding.html',cusname=customer.cname,restadmin = Restadmin.query.all(),chosen=chosen)
            
    return render_template('login.html',cusname="Login failed...\n Please enter valid username and password!")


@app.route("/user-landing", methods=["POST","GET"])
def userLanding():
    if not session.get('cmail'):
        return redirect(request.url_root)
    cmail=session['cmail']
    customer  = Customer.query.filter(Customer.cmail == cmail).first()

    currentDate = datetime.datetime.now()
    month = currentDate.month
    orgs2 = charity_vote.query.filter(charity_vote.month==month).all()
    minds = 0
    spca = 0
    scs = 0
    for i in orgs2:
        if i.organisation == "MINDS":
            minds += 1
        elif i.organisation == "SPCA":
            spca += 1
        elif i.organisation == "SCS":
            scs += 1
    print(minds,spca,scs)
    organisations = ["MINDS", "SPCA", "SCS"]
    charity = [minds,spca,scs]
    chosen=organisations[charity.index(max(charity))]
    print(chosen)
    return render_template('loggedinLanding.html',cusname=customer.cname,restadmin = Restadmin.query.all(),chosen=chosen)


@app.route("/form-submit",methods=["POST","GET"])
def charityform():
    cmail=session['cmail']
    customer=Customer.query.filter(Customer.cmail==cmail).first()
    cid = customer.cid
    

    if request.method == "GET":
        charity = request.args.get("org")
       
        
    
    elif request.method == "POST":
        charity=request.form['org']

    currentDate = datetime.datetime.now()
    month = currentDate.month

    orgs = charity_vote.query.filter(charity_vote.cid == cid).first()
    if orgs and orgs.month == month:
        orgs.organisation = charity
        db.session.commit()
    else:
        # orgs1 = charity_vote(cid=cid,organisation=charity,month=month)
        orgs1 = charity_vote(cid=cid,organisation=charity,month=month)
        db.session.add(orgs1)
        db.session.commit()
    

    orgs2 = charity_vote.query.filter(charity_vote.month==month).all()
    for i in orgs2:
        minds = 0
        spca = 0
        scs = 0
        if i.organisation == "MINDS":
            minds += 1
        elif i.organisation == "SPCA":
            spca += 1
        elif i.organisation == "SCS":
            scs += 1
    organisations = ["MINDS", "SPCA", "SCS"]
    charity = [minds,spca,scs]
    print(charity)
    chosen=organisations[charity.index(max(charity))]
    print(chosen)

    
    # find out most voted charity 
    # reset every month 
    
    return render_template('loggedinLanding.html',cusname=customer.cname,restadmin = Restadmin.query.all(),chosen=chosen)


@app.route('/userprofile')
def userProfile():
    if not session.get('cmail'):
        return redirect(request.url_root)
    cmail=session['cmail']
    customer=Customer.query.filter(Customer.cmail==cmail).first()
    cid = customer.cid
    myorders = Orders.query.filter(Orders.cid==cid).all()
    tprice = 0
    for t in myorders:
        tprice += t.tprice
        tprice = round(tprice,2)

    return render_template('profile2.html',cusname=customer.cname,cusinfo = customer, tprice=tprice)


@app.route('/edituserprofile')
def edituserProfile():
    if not session.get('cmail'):
        return redirect(request.url_root)
    cmail=session['cmail']
    customer=Customer.query.filter(Customer.cmail==cmail).first()
    return render_template('editprofile.html',cusname=customer.cname,cusinfo = customer)

@app.route('/changepass',methods=['POST','GET'])
def changepass():
    if not session.get('cmail'):
        return redirect(request.url_root)
    cmail = session['cmail']
    customer=Customer.query.filter(Customer.cmail==cmail).first()

    return render_template('changepass.html', info=customer)

@app.route('/changepassnext', methods=['POST','GET'])
def changepassnext():
    if request.method == 'POST':

        cmail = request.form['mail1']
        cpassword = request.form['password1']
    elif request.method == "GET":
        cmail = request.args.get("mail1")
        cpassword = request.args.get("password1")


    customer  = Customer.query.filter(Customer.cmail == cmail).first()
    pw_storedhash = customer.cpassword
    if customer and bcrypt.checkpw(cpassword.encode(),pw_storedhash):
            return render_template('changepassnext.html')
    else:
        customer=Customer.query.filter(Customer.cmail==cmail).first()
        return render_template('changepass.html', info=customer,cmsg="Invalid password entered")

@app.route('/updatepassword',methods=['POST','GET'])
def updatepassword():
    if request.method == 'POST':


        cpassword = request.form['cpassword']
        cpassword2 = request.form['cpassword2']
    elif request.method == "GET":

        cpassword = request.args.get("cpassword")
        cpassword2 = request.args.get("cpassword2")
    
    if cpassword == cpassword2:
        cmail=session['cmail']
        customer = Customer.query.filter(Customer.cmail==cmail).first()
        salt = bcrypt.gensalt(rounds=14)
        pwhash = bcrypt.hashpw(cpassword.encode(),salt)
        customer.cpassword=pwhash
        db.session.commit()
        return render_template('changepassnext.html',cmsg1="Sucessfully updated password")
    else:
        return render_template('changepassnext.html',cmsg2="Passwords do not match")

@app.route('/forgorpassword',methods=["POST","GET"])
def forgorpassword():
    if request.method == "GET":
        cmail = request.args.get("cmail")

    
    elif request.method == "POST":
        cmail = request.form['cmail']


        
    new_pass = random.randint(100,999)
    customer=Customer.query.filter(Customer.cmail==cmail).first()
    return render_template('forgorpassword.html',temppass=new_pass)



@app.route('/forgorNext', methods = ['GET','POST'])
def forgorpasswordNext():
    if request.method == "GET":
        temppass = request.args.get("temp")

    
    elif request.method == "POST":
        temppass = request.form['temp']
   
 
    cemail = request.form["cmail"]

    customer=Customer.query.filter(Customer.cmail==cemail).first()
    cmail = customer.cmail
    # send pin to email
   
    # customer.cpassword = temppass
    msg = Message("Hello from Chow Down! Here is your pin to reset your password.", sender="chowdownadmin054@gmail.com", recipients=[cmail])
    msg.body = "Your PIN: " + str(temppass)
    mail.send(msg)
    db.session.commit()
    session['cmail'] = cmail
    return render_template('forgorpasswordNext.html', cusinfo = customer,temppass=temppass)

@app.route('/verify', methods=['POST','GET'])
def verifiy():
    if request.method == "GET":
        temppass = request.args.get("temp")
        pin = request.args.get("pin")
    
    elif request.method == "POST":
        temppass = request.form['temp']
        pin = request.form['pin']

    if temppass == pin:
        return render_template("changepassnext.html")
    else:
        return render_template("forgorpasswordNext.html",cmsg="Pin is incorrect. Please try again")
    
@app.route('/edituserprofileNext', methods = ['GET','POST'])
def edituserprofileNext():
    if not session.get('cmail'):
        return redirect(request.url_root)
    cmail=session['cmail']
    user_name = request.form["name"]
    email_address = request.form["email"]
    address = request.form["address"]
    mobile = request.form["mobile"]
    cid = request.form['cid']
    customer=Customer.query.filter(Customer.cid==cid).first()
    customer.cmail = email_address
    customer.cname = user_name
    customer.cmobile = mobile
    customer.caddress = address

    db.session.commit()
    flash("Successfully updated profile")
    return render_template('profile2.html', cmsg="Passsword Updated Succcessfully...!", cusinfo = customer)




# @app.route("/payment", methods=["GET","POST"])
# def finalpayment():
#     if request.method == "GET":
#         tprice = request.args.get("tprice")
#         items = request.args.get("items")
#         rid=request.args.get("restid")
        
    
#     elif request.method == "POST":
#         tprice=request.form['tprice']
#         items=request.form["items"]
#         rid=request.form['restid']

        
#     return render_template('payment.html', rid=rid,tprice=tprice,items=items)




@app.route("/givereview", methods=["POST","GET"])
def givereview():
    if request.method == "GET":
        tprice = request.args.get("tprice")
        items = request.args.get("items")
        rid=request.args.get("restid")
        paymentType =  request.args.get("pay")
        
    
    elif request.method == "POST":
        tprice=request.form['tprice']
        items=request.form["items"]
        rid=request.form['restid']
        paymentType =  request.form["pay"]
   
        
    cmail=session['cmail']
    customer  = Customer.query.filter(Customer.cmail == cmail).first()
    restadmin  = Restadmin.query.filter(Restadmin.rid == rid).first()
    rid=restadmin.rid
    rname= restadmin.rname
    currentDate = datetime.datetime.now()
    #change to show how month work for graph
    month = currentDate.month
    currentDate = datetime.datetime.now()
    year = currentDate.year
    orders = Orders(cid=customer.cid, rid=rid, items=items,tprice=tprice,payment=paymentType,month1=month,rname=rname)
    # data = Data(rid=rid, month=month, year=year)
    cid = customer.cid
    
    
    if orders :
        db.session.add(orders)
        db.session.commit()
        # db.session.add(data)
        # db.session.commit()
    # restadmin  = Restadmin.query.filter(Restadmin.rid == rid).first()
    return render_template('givereview.html', rid = rid,rname=rname,cid=cid)

@app.route("/givereviewnext", methods=["POST","GET"])
def givereviewnext():
    if request.method == "GET":
        star_rating = request.args.get('rating')
        review = request.args.get('review')
        rid=request.args.get("restid")
        cid = request.args.get("cid1")
    elif request.method == "POST":
        star_rating = request.form['rating']
        review = request.form['review']
        rid=request.form['restid']
        cid = request.form['cid1']
    currentdate = datetime.datetime.now()
    month = currentdate.month
    day = currentdate.day
    year = currentdate.year
    customer = Customer.query.filter(cid==cid).first()
    cname = customer.cname 
    if month == 1:
        month = "January"
    if month == 2:
        month = "February"
    if month == 3:
        month = "March"
    if month == 4:
        month = "April"
    if month == 5:
        month = "May"
    if month == 6:
        month = "June"
    if month == 7:
        month = "July"
    if month == 8:
        month = "August"
    if month == 9:
        month = "September"
    if month == 10:
        month = "October"
    if month == 11:
        month = "November"
    if month == 12:
        month = "December"
    date = month + " " + str(day) +", " + str(year)
    print(star_rating)
    restadmin  = Restadmin.query.filter(Restadmin.rid == rid).first()
    rating = Rating(rstar = star_rating, rreview = review, rid=rid,date=date,cname=cname)
    
    # restadmin.rreview = review
    # restadmin.rstar = star_rating
    db.session.add(rating)
    db.session.commit()
    print("success")
    return render_template("givereview.html",review=review)
    # return redirect(url_for('givereviewnext'))

@app.route("/buyHistory")
def buyHistory():
    if not session.get('cmail'):
        return redirect(request.url_root)
    cmail=session['cmail']
    customer = Customer.query.filter(Customer.cmail == cmail).first()
    cid=customer.cid
    myorders = Orders.query.filter(Orders.cid == cid).all()
    print(myorders)
    totalprice = 0
    for o in myorders:
        print(o.payment)
        
    for i in myorders:
        totalprice += i.tprice
     
    
    return render_template("buyhistory.html", cusname=customer.cname, myorder=myorders, totalprice=round(totalprice,2))




@app.route('/logout')
def logout():
    session.pop('cmail',None)
    return redirect(url_for('landingPage'))
@app.route('/logoutrest')
def logoutrest():
    session.pop('rmail',None)
    return redirect(url_for('landingPage'))
# if __name__ == "__main__":
#     app.run(debug=True)
 