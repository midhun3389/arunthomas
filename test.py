import pandas as pd
import numpy as np
import pickle
import streamlit as st
from PIL import Image
  
# loading in the model to predict on the data
# pickle_in = open('classifier.pkl', 'rb')
# classifier = pickle.load(pickle_in)
  
def welcome():
    return 'welcome all'

  
# this is the main function in which we define our webpage 
def main():
    global output
      # giving the webpage a title
    st.title("Web application")
      
    # here we define some of the front end elements of the web page like 
    # the font and background color, the padding and the text to be displayed
    html_temp = """
    <div style ="background-color:yellow;padding:13px">
    <h1 style ="color:black;text-align:center;">Delivery Delay Prediction APP </h1>
    </div>
    """
      
    # this line allows us to display the front end aspects we have 
    # defined in the above code
    st.markdown(html_temp, unsafe_allow_html = True)
      
    # the following lines create text boxes in which the user can enter 
    # the data required to make the prediction

    Type = st.selectbox("1.Type",("DEBIT","PAYMENT","TRANSFER","CASH") )
    Days_for_shipment = st.number_input("2.Days for shipment (scheduled)",0,10) #options=[0,1,2,3,4,5,6,7,8,9,10])
    Sales_per_customer= st.number_input("3.Sales per customer",7.00,1940.00,step=0.01)
    Category_Id = st.number_input("4.Category Id", 2,76)
    CustomerSegment = st.selectbox("5.CustomerSegment",("Consumer","Corporate","Home Office"))
    Department_Id = st.number_input("6.Department Id",2,12)
    Latitude = st.number_input("7.Latitude",-33.0000,50.0000,step=0.0001)
    Longitude = st.number_input("8.Longitude",-158.0000,116.0000,step=0.0001)
    Market = st.selectbox("9.Market",("LATAM","Europe","Pacific Asia","USCA","Africa"))
    Order_date = st.text_input("order date ","1/17/2018 12:06")
    OrderCity = st.selectbox("10.OrderCity",("Bekasi","Bikaner","Santo Domingo","New York City","Los Angeles","Tegucigalpa","Managua""Aix-les-Bains","patinga","Iringa","Midyat","Yanji"))
    Order_Country = st.selectbox("11.Order Country",("India","China","Estados Unidos","México","Francia","Alemania","Australia","Eritrea","Sáhara Occidental","Burundi","Serbia"))
    # Order_day = st.text_input("12.order day","Type Here")
    # Order_month = st.text_input("13.order month","Type Here")
    # Shipping_day =st.text_input("14.shipping day","Type Here")
    # Shipping_month = st.text_input("15.shipping month","Type Here")
    Order_Item_Discount = st.number_input("16.Order Item Discount",0,500)
    Order_Item_Quantity = st.number_input("17.Order Item Quantity",1,5)
    Order_Profit_Per_Order = st.number_input("18.Order Profit Per Order",-4274.00,912.00,step=0.01)
    OrderRegion = st.selectbox("19.OrderRegion",("Central America","Western Europe","South America","Oceania","Northern Europe","Southeast Asia","Southern Europe","Caribbean","West of USA","South Asia","Eastern Asia","East of USA","West Asia","US Center","South of  USA","Eastern Europe","West Africa"))
    OrderState = st.selectbox("20.OrderState",("Queensland","Tokio","Inglaterra","California","Isla de Francia","Renania del Norte-Westfalia","San Salvador","Pernik","Suceava","Serbia Central","Rajastán"))
    OrderStatus = st.selectbox("21.OrderStatus",("COMPLETE","PENDING","PENDING_PAYMENT","PROCESSING","CLOSED","ON_HOLD","SUSPECTED_FRAUD","CANCELED","PAYMENT_REVIEW"))
    ShippingMode = st.selectbox("22.ShippingMode",("First Class","Standard Class","Second Class","Same Day"))
    Shipping_date = st.text_input("shipping date (DateOrders)","1/17/2018 12:06")
  

    # Featurelist = {"Type":Type,"Days_for_shipment":[Type,Days_for_shipment],"Sales_per_customer":Sales_per_customer,"Category_Id":Category_Id,"CustomerSegment":CustomerSegment,
    #                 "Department_Id":Department_Id,"Latitude":Latitude, "Longitude":Longitude,"Market":Market,"Order_date":Order_date,"OrderCity":OrderCity,
    #                 "Order_Country":Order_Country,"Order_day":Order_day,"Order_month":Order_month,"Shipping_day":Shipping_day,"Shipping_month":Shipping_month,
    #                 "Order_Item_Discount":Order_Item_Discount,"Order_Item_Quantity":Order_Item_Quantity,"Order_Profit_Per_Order":Order_Profit_Per_Order,
    #                 "OrderRegion":OrderRegion,"OrderState":OrderState,"OrderStatus":OrderStatus,"ShippingMode":ShippingMode}
    Featurelist = {"Type":Type,"Days for shipment (scheduled)":Days_for_shipment,"Sales per customer":Sales_per_customer,"Category Id":Category_Id,"CustomerSegment":CustomerSegment,
                    "Department Id":Department_Id,"Latitude":Latitude, "Longitude":Longitude,"Market":Market,"order date ":Order_date,"OrderCity":OrderCity,
                    "Order Country":Order_Country,"Order Item Discount":Order_Item_Discount,"Order Item Quantity":Order_Item_Quantity,"Order Profit Per Order":Order_Profit_Per_Order,
                    "OrderRegion":OrderRegion,"OrderState":OrderState,"OrderStatus":OrderStatus,"ShippingMode":ShippingMode,"shipping date (DateOrders)":Shipping_date}


    # result =""
      
    # the below line ensures that when the button called 'Predict' is clicked, 
    # the prediction function defined above is called to make the prediction 
    # and store it in the variable result
    if st.button("Predict"):

        df = pd.DataFrame(Featurelist,index=[0])  
        
        # df = df.drop(0)
        st.write(df)
        
        # st.write(df) df['order date '] = pd.to_datetime(df['order date '])
        df['shipping date (DateOrders)'] = pd.to_datetime(df['shipping date (DateOrders)'])
        # df['order year'] = pd.DatetimeIndex(df['order date ']).year
        df['order month'] = pd.DatetimeIndex(df['order date ']).month
        df['order day'] = pd.DatetimeIndex(df['order date ']).day
        # df['Shipping year'] = pd.DatetimeIndex(df['shipping date (DateOrders)']).year
        df['Shipping month'] = pd.DatetimeIndex(df['shipping date (DateOrders)']).month
        df['Shipping day'] = pd.DatetimeIndex(df['shipping date (DateOrders)']).day

        df = df.dropna()
        # df_select=df.drop(['Days for shipping (real)','Customer Email','Customer Fname','Customer Id','Customer Lname','Customer Password','CustomerStreet','Customer Zipcode','Order Customer Id','Order Id','Order Item Cardprod Id','Product Card Id','Product Image',"Delivery Status","Category Id","Order Item Id","Product Category Id","Product Status"],axis=1)
        # df=df.drop(["Delivery Status","Category Name","Customer Email","Customer Fname","Customer Lname","Customer Password","CustomerStreet","Department Name","Product Image","Product Name","Order Item Discount Rate"],axis=1)
        df = df[~((df["OrderStatus"] == "SUSPECTED_FRAUD") |(df["OrderStatus"] =="CANCELED"))]#delivery wont happen in these cases
        # df=df.drop(["Product Category Id","Product Card Id","Order Item Cardprod Id","Benefit per order","Order Item Profit Ratio","Product Price","Order Item Total","Sales","Order Item Product Price","Order Item Id","Order Customer Id","Days for shipping (real)","Product Status","CustomerCity","Customer Country","CustomerState","Customer Zipcode","Customer Id","Order Id"],axis=1)
        # order =["Home Office","Consumer","Corporate"]
        # CS = OrdinalEncoder(categories=[order])
        # CS.fit(df[['CustomerSegment']])
        # df["CustomerSegment"]=CS.transform(df[['CustomerSegment']])
        # print(df['CustomerSegment'])
        with open("CS.pkl","rb") as file:
            CS = pickle.load(file)
        df["CustomerSegment"]=CS.transform(df[['CustomerSegment']])    
            
            
        # SMode =["First Class","Second Class","Same Day","Standard Class"]
        # SM = OrdinalEncoder(categories=[SMode])
        # SM.fit(df[['ShippingMode']])
        # df["ShippingMode"]=SM.transform(df[['ShippingMode']])
        # with open("SM.pkl","wb") as file:
        #     pickle.dump(SM,file)
        with open("SM.pkl","rb") as file:
            SM = pickle.load(file)
        df["ShippingMode"]=SM.transform(df[['ShippingMode']])     
            
        # mket =["Europe","Pacific Asia","USCA","Africa","LATAM"]
        # M = OrdinalEncoder(categories=[mket])
        # M.fit(df[['Market']])
        # df["Market"]=M.transform(df[['Market']])
        # with open("M.pkl","wb") as file:
        #     pickle.dump(M,file)
        with open("M.pkl","rb") as file:
            M = pickle.load(file)
        df["Market"]=M.transform(df[['Market']])
            
        # Type =["PAYMENT","DEBIT","CASH","TRANSFER"]
        # T = OrdinalEncoder(categories=[Type])
        # T.fit(df[['Type']])
        # df["Type"]=T.transform(df[['Type']])
        # with open("T.pkl","wb") as file:
        #     pickle.dump(T,file)
        with open("T.pkl","rb") as file:
            T = pickle.load(file)
        df["Type"]=T.transform(df[['Type']])

        with open("OR.pkl","rb") as file:
            OR = pickle.load(file)
        df['OrderRegion_encoder'] = OR.transform(df['OrderRegion'])

        with open("OS.pkl","rb") as file:
            OS = pickle.load(file)
        df['OrderState_encoder'] = OS.transform(df['OrderState'])

        with open("OC.pkl","rb") as file:
            OC = pickle.load(file)
        df['OrderCountry_encoder'] = OC.transform(df['Order Country'])

        with open("ORC.pkl","rb") as file:
            ORC = pickle.load(file)
        df['OrderCity_encoder'] = ORC.transform(df['OrderCity'])

        df['Department Id']= df['Department Id'].map(str)
        df["Category Id"]=df['Category Id'].map(str)

        with open("DI.pkl","rb") as file:
            DI = pickle.load(file)
        df['Department_id_encoded'] = DI.transform(df['Department Id'])


        with open("CI.pkl","rb") as file:
            CI = pickle.load(file)
        df['Category_id_encoded'] = CI.transform(df['Category Id'])

        Q3 = df["Sales per customer"].quantile(.75)
        Q1 = df["Sales per customer"].quantile(.25) 
        IQR=Q3-Q1 
        df = df[~((df["Sales per customer"] < (Q1 - 1.5 * IQR)) |(df["Sales per customer"] > (Q3 + 1.5 * IQR)))]
        Q3 = df["Latitude"].quantile(.75)
        Q1 = df["Latitude"].quantile(.25) 
        IQR=Q3-Q1 
        df = df[~((df["Latitude"] < (Q1 - 1.5 * IQR)) |(df["Latitude"] > (Q3 + 1.5 * IQR)))]
        Q3 = df["Order Profit Per Order"].quantile(.75)
        Q1 = df["Order Profit Per Order"].quantile(.25) 
        IQR=Q3-Q1 
        df = df[~((df["Order Profit Per Order"] < (Q1 - 1.5 * IQR)) |(df["Order Profit Per Order"] > (Q3 + 1.5 * IQR)))]
        with open("transformer.pkl","rb") as file:
            transformer = pickle.load(file)
        df=transformer.transform(df)            

        

        with open('model.pkl','rb') as file:

            model = pickle.load(file)
            output = model.predict(df)
            

        # result = prediction(sepal_length, sepal_width, petal_length, petal_width)
        st.title("PREDICTION")
        if output ==1:
            st.success('There is a possibility of late delivery of the order')
        else:
        
            st.success('Order is on time')
    
if __name__=='__main__':
    main()
