from . import _except_return_none

@_except_return_none
def get_dataframe_manifest(df):

    try:
        # left-align unique counts
        max_col_len = max( len(col) for col in df.columns )
        pad = lambda col: (max_col_len - len(col)) * ' '
        nunique = {
            col :
                pad(col)
                + f' {df[col].nunique(dropna=True)}#'
                + ( f',{df[col].isna().sum()}na' if df[col].hasnans else '' )
            for col in df.columns
        }

        # left-align example values
        max_len = max(
            len(col) + len(uniqstr) for col, uniqstr in nunique.items()
        )
        pad = lambda col, uniqstr: (max_len - len(col) - len(uniqstr)) * ' '
        return {
            col : nunique[col] + pad(col, nunique[col]) + '  ex., ' + str(val)
            for col, val in df.dropna().to_dict( orient='records' )[0].items()
        }

    except IndexError:
        return list( df.columns )
