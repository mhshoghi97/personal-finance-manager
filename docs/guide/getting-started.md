
## **Step 3: Creating the Configuration File**

### **3.1 Creating the `mkdocs.yml` File**

* In the root directory of your project, create a file named **`mkdocs.yml`**.
* Insert the following basic content into the file:

---


```yaml
site_name: MhShoghi Financial Manager
site_description: Documentation for the Financial Management System

theme:
  name: material

nav:
 - Home: index.md
  - Guide:
      - Installation: guide/installation.md
      - Getting Started: guide/getting-started.md
  - Functions: reference/functions.md

