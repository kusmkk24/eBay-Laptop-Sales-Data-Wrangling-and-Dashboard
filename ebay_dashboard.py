import pandas as pd
import streamlit as st
import plotly.express as px

df = pd.read_csv('/Users/karol/Downloads/Data Management/eBay Dashboard/EbayCleanedDataSample.csv')
newdf = df.drop("Unnamed: 0", axis='columns')
newdf['Item Number'] = newdf['Item Number'].astype(str)
#print(newdf)

newdf['Condition'].replace(to_replace=['UsedAn item that has been used previously. The item may have some signs of cosmetic wear, but is fully operational and functions as intended. This item may be a floor model or store return that has been used. See the seller’s listing for full details and description of any imperfections. See all condition definitionsopens in a new window or tab'], 
       value='Used: An item that has been used previously. The item may have some signs of cosmetic wear, but is fully operational and functions as intended. This item may be a floor model or store return that has been used. See the seller’s listing for full details and description of any imperfections. See all condition definitionsopens in a new window or tab', inplace=True)
newdf['Condition'].replace(to_replace=["Open boxAn item in excellent, new condition with no wear. The item may be missing the original packaging or protective wrapping, or may be in the original packaging but not sealed. The item includes original accessories. The item may be a factory second. See the seller's listing for full details and description. See all condition definitionsopens in a new window or tab"], 
       value="Open box: An item in excellent, new condition with no wear. The item may be missing the original ...  Read moreabout the conditionOpen box: An item in excellent, new condition with no wear. The item may be missing the original packaging or protective wrapping, or may be in the original packaging but not sealed. The item includes original accessories. The item may be a factory second. See the seller's listing for full details and description. See all condition definitionsopens in a new window or tab ", inplace=True)
newdf['Condition'].replace(to_replace=['For parts or not workingAn item that does not function as intended and is not fully operational. This includes items that are defective in ways that render them difficult to use, items that require service or repair, or items missing essential components. See the seller’s listing for full details. See all condition definitionsopens in a new window or tab'], 
       value='For parts or not working: An item that does not function as intended and is not fully operational. ...  Read moreabout the conditionFor parts or not working: An item that does not function as intended and is not fully operational. This includes items that are defective in ways that render them difficult to use, items that require service or repair, or items missing essential components. See the seller’s listing for full details. See all condition definitionsopens in a new window or tab ', inplace=True)

def extract_before_special_char(text):
    # Split the string at the first occurrence of ":" or " - "
    if " - " in text:
        return text.split(" - ")[0]
    elif ":" in text:
        return text.split(":")[0]
    else:
        return text  # If no special character, return the whole text

# Apply the function to the dataframe column
newdf['Condition'] = newdf['Condition'].apply(extract_before_special_char)

st.set_page_config(layout="wide")
st.title("eBay Laptop Sales")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Orignial Data", "Filtered Data", "Laptop Conditions", "Price Ranges", "Brand Price Ranges"])

with tab1:
    st.subheader("Original Data:")
    st.dataframe(newdf, use_container_width=True)
    st.write('This data describes all laptops and their attributes that were sold in the past year on eBay.')

with tab2:
    # create column layout
    #col1, col2, col3, col4 = st.columns(4)
    # input min and max values for price filtration in column layout
    #with col1:
    #brand_filter = st.selectbox("Select a brand: ", options = ["All"] + newdf['Brand'].unique().tolist(),key="brand_filter")
    brands = newdf['Brand'].unique()
    container = st.container()
    all = st.checkbox("Select all", key="brand_all")

    if all:
        brand_selection = container.multiselect("Select one or more brands or select all:",
        brands,brands)
    else:
        brand_selection = container.multiselect("Select one or more brands or select all:",
        brands)
    #with col2:
    #condition_filter = st.selectbox("Select a condition: ", options = ["All"] + newdf['Condition'].unique().tolist())
    conditions = newdf['Condition'].unique()
    condition_container = st.container()
    condition_all = st.checkbox("Select all", key="condition_all")
 
    if condition_all:
        condition_selection = condition_container.multiselect("Select one or more conditions or select all:",
        conditions,conditions)
    else:
        condition_selection = condition_container.multiselect("Select one or more conditions or select all:",
        conditions)
    col3, col4 = st.columns(2)
    with col3:
        min = st.number_input("Insert minimum number", value=None, placeholder="Type a number...")
    with col4:
        max = st.number_input("Insert maximum number", value=None, placeholder="Type a number...")
    
    filtered_df = newdf.copy()

# displayed filtered df
    if all == True:
        filtered_df = filtered_df  # No filtering
    else:
        filtered_df = filtered_df[filtered_df["Brand"].isin(brand_selection)]
    #if brand_selection != "All":
       # filtered_df = filtered_df[filtered_df["Brand"] == brand_selection]

    #if condition_filter != "All":
    #    filtered_df = filtered_df[filtered_df["Condition"] == condition_filter]

    if condition_all == True:
        filtered_df = filtered_df  # No filtering
    else:
        filtered_df = filtered_df[filtered_df["Condition"].isin(condition_selection)]

    if min is not None and max is not None and min < max and min>=0: 
        filtered_df = filtered_df[(filtered_df['Price'] >= min) & (filtered_df['Price'] <= max)]
        st.subheader("Filtered DataFrame by Brand, Condition, and Price Range:")
        st.dataframe(filtered_df)
        st.write('This data describes laptops and their attributes that were sold in the past year on eBay based on the selected filters.')
    else:
        st.error("Please select a valid price range.")

with tab3:
    st.subheader("Number of Laptops per Condition")
    condition_count = newdf['Condition'].value_counts(sort=True)
    
    st.bar_chart(condition_count, height = 300, horizontal=True)

    st.markdown('''This chart shows how many laptops fall into each condition category, such as new, used, or refurbished. 
    It provides a straightforward way to understand the composition of the listings or sales. 
    This information is valuable for understanding consumer behavior and inventory trends. 
    For example, a majority of laptops are used, which might indicate a stronger demand for affordable options over brand-new devices. 
    This insight could guide targeted marketing campaigns or inform sourcing strategies. 
    Promoting refurbished laptops as cost-effective, high-value alternatives could attract budget-conscious customers. 
    Similarly, if new laptops were to dominate, we may need to highlight premium features and warranties to capitalize on the trend.''')
    


with tab4:
    st.subheader('Distribution of Laptop Prices')
    fig = px.histogram(newdf, x="Price",
                   labels={'Price':'Dollars'}, # can specify one label per df column
                   #opacity=0.8,
                   #color_discrete_sequence=['indianred'] # color of histogram bars
                   )
    fig.update_layout(bargap=0.05, xaxis_title= "Price in Dollars", yaxis_title= "Laptops", height = 500)

    st.plotly_chart(fig)
    st.markdown('''This histogram of laptop prices provides an overview of the most common price ranges and how prices are distributed across the dataset. 
    This visualization is critical for identifying pricing trends, such as clusters of listings in specific price brackets or gaps in pricing. 
    Understanding these patterns will help us to position our products competitively within the market. 
    If most laptops are priced in the mid-range, we might focus on emphasizing unique features to differentiate products in this crowded segment. 
    Alternatively, if there’s a gap in the market for high-end or low-cost laptops, we could adjust our inventory or pricing strategies to fill those gaps, and maximize on the potential revenue.''')
    
with tab5:
   
    #brand_box = st.selectbox("Select a brand: ", options = ["All"] + newdf['Brand'].unique().tolist(),key="brand_box")
    brands = newdf['Brand'].unique()
    box_container = st.container()
    box_all = st.checkbox("Select all", key="box_all")
 
    if box_all:
        box_selection = box_container.multiselect("Select one or more brands:",
        brands,brands, key='box_brands')
    else:
        box_selection = box_container.multiselect("Select one or more brands:",
        brands, key='box_brands')
    
    st.subheader('Laptop Price Ranges per Brand')
    filtered_box_df = newdf.copy()

   # if brand_box != "All":
   #     filtered_box_df = filtered_box_df[filtered_box_df["Brand"] == brand_box]

    if box_all == True:
        filtered_box_df = filtered_box_df  # No filtering
    else:
        filtered_box_df = filtered_box_df[filtered_box_df["Brand"].isin(box_selection)]
   
    box = px.box(filtered_box_df, x="Brand", y="Price")
    box.update_layout(yaxis_title= "Price in Dollars", xaxis_title= "Brand(s)",  width = 3000, height = 600)
    st.plotly_chart(box)
    st.markdown('''The box plot compares laptop prices across the selected brands and provides a clear view of the price distribution for each selected brand. 
    It highlights the minimum, maximum, median, and interquartile ranges, offering insights into how brands are positioned in the market in terms of pricing. 
    Premium brands typically show higher median prices and narrower ranges, indicating a focus on high-end consumers. 
    Alternatively, more affordable brands often have wider price ranges and lower medians, appealing to budget-conscious buyers. 
    This helps inform inventory and marketing strategies by aligning product positioning with customer expectations, whether focusing on premium quality or being budget friendly.''')
    
    
    





