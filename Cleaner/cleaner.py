
class Cleaner():
    def __init__(self):
        pass

    def clean_dataframe(self,df):
        df.dropna(axis=1, inplace=True)

        # keeping the last column of links and rejecting the second last column of useless data

        # ['Sl no.', 'Diarrhea no.', 'diarrhea type', 'Du. Prohibit. Office','Year', 'Will write', 'Will write down', 'Other information','List no. 2']
        drop_col = df.columns[-2]
        df.drop(columns=drop_col, inplace=True)
        df.rename(columns={'link':drop_col}, inplace=True)

        # renaming the anomalies in the columns
        df.rename(columns={
            df.columns[0]:'sr_no',
            df.columns[1]:'doc_no',
            df.columns[2]:'doc_type',
            df.columns[3]:'dn_office',
            df.columns[4]:'doc_date',
            df.columns[5]:'buyer_name',
            df.columns[6]:'seller_name',
            df.columns[7]:'other_info',
            df.columns[8]:'list_two_link'
        }, inplace=True)

        """
        ['lease', 'In the development agreement', 'sale deed',
            'Section 66 - Notice of lie pendency',
            '65-error correction letter', 'Development Agreement',
            'Deed of Transfer', 'affidavit', 'leasedeed', '59-Transfer',
            'prize certificate', 'declaration', 'Live Ad Licenses',
            'transfer deed', 'Agreement', '36-A-Live Ad Licenses',
            'Bill of Sale', 'Amphideviate']
        Unique values need to be tweaked for better readability
        """
        df.replace(to_replace='Amphideviate', value='affidavit', inplace=True)
        df.replace(to_replace='Deed of Transfer', value='transfer deed', inplace=True)
        df.replace(to_replace='leasedeed',value='lease deed',inplace=True)
        df.replace(to_replace='Section 66 - Notice of lie pendency', value='Notice of lease pendency', inplace=True)

        # columns have datatypes of object and float64, need conventional form of dtypes
        for col in df.columns:
            if df[col].dtype == 'float64':
                df[col] = df[col].astype('int32')

        # converting doc_date from string object to datetime object
        try:
            df['doc_date'] = pd.to_datetime(df['Year'],format='mixed')
        except:
            ValueError('Not in correct format')
        
        return df