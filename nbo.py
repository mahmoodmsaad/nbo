import streamlit as st
import pandas as pd

def load_data(file_path):
    return pd.read_csv(file_path)

def filter_data(data, ignore_values, top_n, ascending=True):
    # Check if 'Orbital' column is present
    if 'Orbital' not in data.columns:
        st.error("The 'Orbital' column is missing in the DataFrame.")
        return pd.DataFrame()  # Return an empty DataFrame to avoid further errors

    # Ignore rows containing specified values
    for value in ignore_values:
        data = data[data['Orbital'] != value]

    # Check if 'kcal/mol' column is present
    if 'kcal/mol' in data.columns:
        # Display maximum kcal/mol
        max_kcal = data['kcal/mol'].max()
        st.subheader(f"Maximum kcal/mol: {max_kcal}")
    else:
        st.warning("The 'kcal/mol' column is missing in the DataFrame.")

    # Display information about specific orbitals
    orbital_info = {}
    for orbital in ['RY*', 'BD*', 'BD', 'LP', 'CR']:
        if 'Orbital' in data.columns:  # Check again in case the column was removed
            orbital_count = data[data['Orbital'] == orbital].shape[0]
            orbital_info[orbital] = {
                'Count': orbital_count,
                'Rows': data[data['Orbital'] == orbital].index.tolist()
            }

    st.subheader("Orbital Information:")
    st.write(orbital_info)

    # Sort by kcal/mol and display top N if 'kcal/mol' column is present
    if 'kcal/mol' in data.columns:
        sorted_data = data.sort_values(by='kcal/mol', ascending=ascending)
        return sorted_data.head(top_n)
    else:
        return pd.DataFrame()

def main():
    st.title("Orbital Energy Analyzer")

    # Upload CSV file
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file is not None:
        data = load_data(uploaded_file)

        # Display raw data
        st.subheader("Raw Data:")
        st.write(data)

        # Ignore specified orbitals
        ignore_values = st.multiselect("Ignore Orbitals:", ['RY*', 'CR', 'LP'])

        # Filter by top or bottom energies
        filter_type = st.radio("Select Filter Type:", ["Top", "Bottom"])
        top_n = st.number_input("Number of Orbitals to Display:", min_value=1, max_value=len(data), value=10)

        if filter_type == "Top":
            st.subheader(f"Top {top_n} Orbitals:")
            result = filter_data(data, ignore_values, top_n)
        else:
            st.subheader(f"Bottom {top_n} Orbitals:")
            result = filter_data(data, ignore_values, top_n, ascending=False)

        st.write(result)

if __name__ == "__main__":
    main()
