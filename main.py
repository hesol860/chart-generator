# import streamlit
import streamlit as st
import matplotlib.pyplot as plt
from io import BytesIO
import base64
# from PIL import Image


# Database
if 'datasets' not in st.session_state:
    st.session_state.datasets = []

# Title
st.set_page_config(page_title="Dynamic Chart Generator", layout="centered")

if "chart_data" not in st.session_state:
    st.session_state.chart_data = []
if "compare_mode" not in st.session_state:
    st.session_state.compare_mode = False

# Logo


col_logo1, col_space, col_logo2 = st.columns([1, 6, 1])

with col_logo1:
    st.image("logo1.png", use_container_width=True)


with col_space:
    st.markdown("<h1 style='text-align: center;'>Chart Generator</h1>", unsafe_allow_html=True)

with col_logo2:
    st.image("logo2.png", use_container_width=True)
    st.markdown("<p style='text-align:center; font-size:14px;'>Solmaz Abedi</p>", unsafe_allow_html=True)

# Chart
st.title("Chart Generator")

if 'sample_name' not in st.session_state:
    st.session_state.sample_name = ""
if 'test_type' not in st.session_state:
    st.session_state.test_type = ""
if 'input_data' not in st.session_state:
    st.session_state.input_data = ""
if 'color' not in st.session_state:
    st.session_state.color = "#0000FF"

if st.session_state.get("edit_mode"):
    idx = st.session_state.edit_index
    dataset = st.session_state.datasets[idx]
    sample_name = st.text_input("Sample Name", value=dataset["sample_name"], key="sample_name_input")
    test_type = st.text_input("Test Type", value=dataset["test_type"], key="test_type_input")
    x_label = st.text_input("X-Axis Label", value=st.session_state.get("x_label_input", ""), key="x_label_input")
    y_label = st.text_input("Y-Axis Label", value=st.session_state.get("y_label_input", ""), key="y_label_input")
    input_data = st.text_area("Enter data (format: label=value,label=value,...)",
                              value=",".join([f"{k}={v}" for k, v in dataset["data"].items()]),
                              key="input_data_input", height=100)
    color = st.color_picker("Choose Chart Color", value=dataset.get("color", "#0000FF"), key="color_input")
else:
    sample_name = st.text_input("Sample Name", value=st.session_state.get("sample_name_input", ""),
                                key="sample_name_input")
    test_type = st.text_input("Test Type", value=st.session_state.get("test_type_input", ""), key="test_type_input")
    x_label = st.text_input("X-Axis Label", value=st.session_state.get("x_label_input", ""), key="x_label_input")
    y_label = st.text_input("Y-Axis Label", value=st.session_state.get("y_label_input", ""), key="y_label_input")
    input_data = st.text_area("Enter data (format: label=value,label=value,...)",
                              value=st.session_state.get("input_data_input", ""),
                              key="input_data_input", height=100)
    color = st.color_picker("Choose Chart Color", value=st.session_state.get("color_input", "#0000FF"),
                            key="color_input")

if st.button("Add to Compare"):
    data_dict = {}
    for item in input_data.split(','):
        if '=' in item:
            k, v = item.strip().split('=')
            data_dict[k.strip()] = float(v.strip())

    if len(st.session_state.datasets) < 5:
        st.session_state.datasets.append({"data": data_dict, "color": color,
                                          "sample_name": sample_name, "test_type": test_type
                                          })
    else:
        st.warning("You can compare only 5 charts")
    st.session_state.compare_mode = True

st.markdown("### Edit a Chart")

for i, d in enumerate(st.session_state.datasets):
    col1, col2 = st.columns([6, 1])
    with col1:
        st.write(f"**{i + 1}.** {d['sample_name']} - {d['test_type']}")
    with col2:
        if st.button(f"✏️ Edit {i + 1}", key=f"edit_{i}"):
            st.session_state.edit_index = i
            st.session_state.edit_mode = True

chart_type = st.selectbox(
    "Select Chart Type", ["Line", "Bar", "Column", "Scatter", "Stem", "Area",
                          "Pie", "Combo", "Radar"])
chart_type = chart_type.lower()

col1, col2 = st.columns(2)
generate = col1.button("Generate Chart")
reset = col2.button("Reset")


if generate:
    data_dict = {}
    for item in input_data.split(','):
        if '=' in item:
            k, v = item.strip().split('=')
            try:
                data_dict[k.strip()] = float(v.strip())
            except ValueError:
                st.warning("Please enter a valid value")
                data_dict = {}
                break

    if data_dict:
        st.session_state.datasets = [{"data": data_dict, "color": color,
                                      "sample_name": sample_name, "test_type": test_type
                                      }]
        st.session_state.compare_mode = False

if st.session_state.get("edit_mode"):
    if st.button("💾 Save Edit"):
        data_dict = {}
        for item in st.session_state.input_data_input.split(','):
            if '=' in item:
                try:
                    k, v = item.strip().split('=')
                    data_dict[k.strip()] = float(v.strip())
                except ValueError:
                    st.warning("The data format is incorrect. Please check again")
                    data_dict = {}
                    break

        if data_dict:
            idx = st.session_state.get("edit_index")
            st.session_state.datasets[idx] = {
                "data": data_dict,
                "color": st.session_state.color_input,
                "sample_name": st.session_state.sample_name_input,
                "test_type": st.session_state.test_type_input
            }
            st.success(f"Chart {idx + 1} updated.")
            st.session_state.edit_mode = False

            for key in ["sample_name_input", "test_type_input", "input_data_input", "color_input"]:
                if key in st.session_state:
                    del st.session_state[key]

# if compare:
#     data_dict = {}
#     for item in input_data.split(','):
#         if '=' in item:
#             k, v = item.strip().split('=')
#             try:
#                 data_dict[k.strip()] = float(v.strip())
#             except:
#                 st.warning("An invalid value has been entered.")
#                 data_dict = {}
#                 break
#
#     if data_dict:
#         if len(st.session_state.datasets) < 5:
#             st.session_state.datasets.append(data_dict)
#         else:
#             st.warning("You can compare only 5 charts.")
#         st.session_state.compare_mode = True

if reset:
    st.session_state.datasets = []
    st.session_state.compare_mode = False
    for key in ["sample_name_input", "test_type_input", "x_label_input", "y_label_input", "input_data_input",
                "color_input"]:
        if key in st.session_state:
            del st.session_state[key]

# Draw chart
if st.session_state.datasets:
    colors = ['C0', 'C1', 'C2', 'C3', 'C4']

    # Chart selection
    st.markdown("### Select charts to compare")
    selected_labels = [
        f"{i + 1}. {d['sample_name']} - {d['test_type']}"
        for i, d in enumerate(st.session_state.datasets)
    ]

    selected_options = st.multiselect("Choose which charts to compare:",
                                      options=selected_labels,
                                      default=selected_labels,
                                      key="selected_charts")

    selected_indices = [int(label.split('.')[0]) - 1 for label in selected_options]

    if selected_indices:
        fig, ax = plt.subplots()

        if chart_type in ['radar', 'pie']:
            dataset = st.session_state.datasets[selected_indices[0]]
            data = dataset['data']
            labels = list(data.keys())
            values = list(data.values())

            if chart_type == 'radar':
                values += values[:1]
                angles = [n / float(len(labels)) * 2 * 3.14159265 for n in range(len(labels))]
                angles += angles[:1]

                ax = plt.subplot(111, polar=True)
                ax.plot(angles, values, color=dataset.get('color', 'C0'), label=f"{dataset['sample_name']} - "
                                                                                f"{dataset['test_type']}")
                ax.fill(angles, values, color=dataset.get('color', 'C0'), alpha=0.25)
                ax.set_xticks(angles[:-1])
                ax.set_xticklabels(labels)
                ax.legend()

            elif chart_type == 'pie':
                ax.clear()
                ax.pie(values, labels=labels, autopct='%1.1f%%')

        else:
            # other charts
            for idx in selected_indices:
                dataset = st.session_state.datasets[idx]
                data = dataset['data']
                color = dataset.get('color', colors[idx % len(colors)])
                x = list(data.keys())
                y = list(data.values())
                sample = dataset.get("sample_name", f"Chart {idx + 1}")
                test = dataset.get("test_type", "")
                label = f"{sample} - {test}"

                if chart_type == 'line':
                    ax.plot(x, y, label=label, marker='o', color=color)
                elif chart_type == 'bar':
                    ax.bar([f"{xi}-{idx + 1}" for xi in x], y, label=label, color=color)
                elif chart_type == 'scatter':
                    ax.scatter(x, y, label=label, color=color)
                elif chart_type == 'column':
                    ax.bar(x, y, label=label, color=color)
                elif chart_type == 'combo':
                    ax.bar(x, y, label=f"{label} - Bar", color=color, alpha=0.4)
                    ax.plot(x, y, label=f"{label} - Line", marker='o', color=color)
                elif chart_type == 'stem':
                    ax.stem(x, y, label=label, linefmt=color + '-', markerfmt=color + 'o')
                elif chart_type == 'area':
                    ax.fill_between(x, y, label=label, color=color, alpha=0.3)

            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)
            ax.legend()
            plt.xticks(rotation=45, fontsize=8)

        # download image
        st.pyplot(fig)
        buf = BytesIO()
        fig.savefig(buf, format="jpg")
        buf.seek(0)
        b64 = base64.b64encode(buf.read()).decode()
        href = f'<a href="data:file/jpg;base64,{b64}" download="chart.jpg">📥 Download JPG</a>'
        st.markdown(href, unsafe_allow_html=True)
