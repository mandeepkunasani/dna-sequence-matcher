import streamlit as st
import pandas as pd

st.set_page_config(page_title="Hospital System", layout="wide")

# ---------- SESSION ----------
if "users" not in st.session_state:
    st.session_state.users = {"admin": "admin123"}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "patients" not in st.session_state:
    st.session_state.patients = []

if "resources" not in st.session_state:
    st.session_state.resources = {
        "ICU":10,"Beds":25,"Oxygen":20,"Ventilator":10,
        "Ambulance":5,"ECG":8,"MRI":3,"CT Scan":4,
        "X-Ray":6,"Blood":30,"Dialysis":5,
        "OT":6,"Wheelchair":15,"Stretchers":10,"Monitors":12
    }

# ---------- DOCTORS ----------
doctors = [
{"Name":"Dr. Arjun Reddy","Department":"Cardiology","Role":"Senior Cardiologist"},
{"Name":"Dr. Meera Nair","Department":"Neurology","Role":"Neurosurgeon"},
{"Name":"Dr. Karthik Rao","Department":"Orthopedics","Role":"Orthopedic Surgeon"},
{"Name":"Dr. Priya Sharma","Department":"Pediatrics","Role":"Child Specialist"},
{"Name":"Dr. Rahul Verma","Department":"Oncology","Role":"Cancer Specialist"},
{"Name":"Dr. Sneha Iyer","Department":"Dermatology","Role":"Skin Specialist"},
{"Name":"Dr. Vikas Singh","Department":"ENT","Role":"ENT Surgeon"},
{"Name":"Dr. Ananya Gupta","Department":"Psychiatry","Role":"Psychiatrist"},
{"Name":"Dr. Rohan Das","Department":"Urology","Role":"Urologist"},
{"Name":"Dr. Kavya Menon","Department":"Gynecology","Role":"Gynecologist"},
{"Name":"Dr. Amit Patel","Department":"Radiology","Role":"Radiologist"},
{"Name":"Dr. Neha Kapoor","Department":"Emergency","Role":"Emergency Specialist"},
{"Name":"Dr. Sanjay Kumar","Department":"General","Role":"General Physician"},
{"Name":"Dr. Pooja Jain","Department":"Surgery","Role":"General Surgeon"},
{"Name":"Dr. Imran Ali","Department":"Pulmonology","Role":"Lung Specialist"},
{"Name":"Dr. Deepika Roy","Department":"Nephrology","Role":"Kidney Specialist"},
{"Name":"Dr. Vikram Shah","Department":"Endocrinology","Role":"Diabetes Specialist"},
{"Name":"Dr. Tanvi Desai","Department":"Hematology","Role":"Blood Specialist"},
{"Name":"Dr. Raj Malhotra","Department":"Gastroenterology","Role":"Digestive Specialist"},
{"Name":"Dr. Aisha Khan","Department":"Infectious","Role":"Infection Specialist"}
]

# ---------- LOGIN ----------
if not st.session_state.logged_in:

    st.title("🔐 Hospital Login")

    tab1, tab2 = st.tabs(["Login", "Signup"])

    with tab1:
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")

        if st.button("Login"):
            if user in st.session_state.users and st.session_state.users[user] == pwd:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")

        if st.button("Register"):
            if new_user in st.session_state.users:
                st.error("User exists")
            else:
                st.session_state.users[new_user] = new_pass
                st.success("Registered successfully")

    st.stop()

# ---------- DASHBOARD ----------
st.title("🏥 Hospital Resource Allocation System")

col1,col2,col3 = st.columns(3)
col1.metric("Patients", len(st.session_state.patients))
col2.metric("Resources", len(st.session_state.resources))
col3.metric("Doctors", len(doctors))

# ---------- ADD PATIENT ----------
st.subheader("➕ Add Patient")

c1,c2,c3,c4 = st.columns(4)

name = c1.text_input("Name")
age = c2.number_input("Age",1,100,25)
problem = c3.text_input("Problem")
dept = c4.selectbox("Department",[d["Department"] for d in doctors])

# PRIORITY (manual + AI)
manual_priority = st.selectbox("Select Priority", ["Normal", "Critical"])
keywords = ["critical","emergency","severe","accident"]
auto_priority = "Critical" if any(k in problem.lower() for k in keywords) else "Normal"
st.info(f"AI Suggestion: {auto_priority}")
priority = manual_priority

resources_req = st.multiselect("Required Resources", list(st.session_state.resources.keys()))
need = st.number_input("Units per resource",1,10,1)

doc = next((d for d in doctors if d["Department"]==dept),None)

if st.button("Add Patient"):
    st.session_state.patients.append({
        "Name":name,
        "Age":age,
        "Problem":problem,
        "Department":dept,
        "Doctor":doc["Name"],
        "Role":doc["Role"],
        "Resources":resources_req,
        "Allocated_Resources":[],
        "Need":need,
        "Priority":priority,
        "Allocated":False
    })

# ---------- RESOURCES DISPLAY ----------
st.subheader("🏥 Available Resources")

for r, val in st.session_state.resources.items():
    st.markdown(f"**{r}** : {val}")

# ---------- PATIENT TABLE ----------
st.subheader("🧾 Patient Table")

search = st.text_input("🔍 Search Patient")

if st.session_state.patients:
    df = pd.DataFrame(st.session_state.patients)
    df = df.reset_index().rename(columns={"index":"orig_idx"})

    if search:
        df = df[df["Name"].str.contains(search, case=False)]

    headers = st.columns(13)
    titles = ["Name","Age","Problem","Dept","Doctor","Role",
              "Requested","Allocated","Need","Priority","Status","Actions","Allocate"]

    for col,t in zip(headers,titles):
        col.write(f"**{t}**")

    for _,row in df.iterrows():
        i = int(row["orig_idx"])

        if row["Priority"]=="Critical":
            st.markdown("<div style='background:#7f1d1d;padding:8px;border-radius:8px'>",unsafe_allow_html=True)

        cols = st.columns(13)

        cols[0].write(row["Name"])
        cols[1].write(row["Age"])
        cols[2].write(row["Problem"])
        cols[3].write(row["Department"])
        cols[4].write(row["Doctor"])
        cols[5].write(row["Role"])
        cols[6].write(", ".join(row["Resources"]))
        cols[7].write(", ".join(row["Allocated_Resources"]) if row["Allocated_Resources"] else "-")
        cols[8].write(row["Need"])
        cols[9].markdown("🔴 Critical" if row["Priority"]=="Critical" else "🟢 Normal")
        cols[10].write("✅ Allocated" if row["Allocated"] else "⏳ Pending")

        c1,c2 = cols[11].columns(2)

        if c1.button("➕", key=f"inc_{i}"):
            st.session_state.patients[i]["Need"] += 1
            st.rerun()

        if c2.button("❌", key=f"del_{i}"):
            st.session_state.patients.pop(i)
            st.rerun()

        if cols[12].button("Allocate", key=f"alloc_{i}"):

            p = st.session_state.patients[i]

            if not p["Allocated"]:
                can_allocate = True

                for r in p["Resources"]:
                    if st.session_state.resources[r] < p["Need"]:
                        can_allocate = False
                        break

                if can_allocate:
                    for r in p["Resources"]:
                        st.session_state.resources[r] -= p["Need"]

                    p["Allocated"] = True
                    p["Allocated_Resources"] = p["Resources"]

                    st.success(f"{p['Name']} Allocated ✅")
                else:
                    st.error("Not enough resources ❌")

            st.rerun()

        if row["Priority"]=="Critical":
            st.markdown("</div>",unsafe_allow_html=True)

else:
    st.info("No patients added")

# ---------- RESOURCE CONTROL ----------
st.sidebar.subheader("⚙️ Resource Control")

res_sel = st.sidebar.selectbox("Resource", list(st.session_state.resources.keys()))

set_val = st.sidebar.number_input("Set Value",0,100,st.session_state.resources[res_sel])
if st.sidebar.button("Set"):
    st.session_state.resources[res_sel] = set_val

inc_val = st.sidebar.number_input("Increase",1,50,5)
if st.sidebar.button("Increase"):
    st.session_state.resources[res_sel] += inc_val

# ---------- LOGOUT ----------
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()