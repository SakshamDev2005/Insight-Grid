import io
import pandas as pd
from matplotlib import pyplot as plt
import base64
import matplotlib

matplotlib.use('Agg')  # 👈 Force non-GUI backend


def read_csv_file(uploaded_file):
    """
    Reads a CSV file and returns its content as a dictionary. """

    try:
        # Read CSV directly into pandas
        decoded_file = uploaded_file.read().decode('utf-8')
        df = pd.read_csv(io.StringIO(decoded_file))

        df_dict = df.to_dict(orient='split')

        if df.empty:
            raise ValueError("CSV file is empty or malformed.")

        return df_dict, uploaded_file.name.replace('.csv', '')

    except Exception as e:
        raise Exception(f"Failed to process CSV file: {e}")
    
def generate_plot(table_data, plot_type, x_axis, y_axis):
    try:
        # Create figure and axis
        fig, ax = plt.subplots()

        # Generate the plot based on the type
        if plot_type == 'pie':
            ax.pie(table_data[y_axis], labels=table_data[x_axis], autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        else:
            table_data.plot(x=x_axis, y=y_axis, kind=plot_type, ax=ax)

        # Save to in-memory buffer
        buffer = io.BytesIO()
        plt.tight_layout()  # Adjust layout to prevent clipping
        plt.savefig(buffer, format='png')
        plt.close(fig)  # Close the figure after saving to avoid memory issues

        # Encode to base64
        buffer.seek(0)
        image_png = buffer.getvalue()
        base64_img = base64.b64encode(image_png).decode('utf-8')
        return base64_img
    except Exception as e:
        raise Exception(f"Failed to generate plot: {e}")