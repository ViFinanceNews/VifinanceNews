

# ViFinanceNews 🚀
A financial news analysis tool integrating the **ViFinanceCrawLib** submodule for data extraction.

## 📂 Project Structure




## 🛠️ **Setup and Cloning the Repository**
Since **ViFinanceCrawLib** is a Git **submodule**, you must clone it properly.

### ✅ **Cloning with Submodules**
If you are cloning this repo for the first time, run:
```bash
git clone --recurse-submodules https://github.com/DTJ-Tran/VifinanceNews.git

This will download the main repo and initialize the submodule.

🔄 If You Already Cloned the Repo

If you cloned the repo without --recurse-submodules, initialize and update the submodule manually:

git submodule update --init --recursive

🔄 Pulling Updates for Submodules

When you pull updates from the main repo, also update the submodule:

git pull origin main
git submodule update --recursive --remote

📦 How to Use ViFinanceCrawLib in the Main Module

The ViFinanceCrawLib submodule is located in src/main/resources/ViFinanceCrawLib/.

🏗 Building the Project

Ensure that your project recognizes the submodule:
	•	If using Java & Maven, add the submodule directory to your pom.xml.
	•	If using Python, navigate to the submodule directory and install dependencies:

cd src/main/resources/ViFinanceCrawLib/
pip install -r requirements.txt



📜 Importing the Submodule in Your Code
	•	Java Example (if applicable):

import com.vifinancecrawlib.DataExtractor;

public class Main {
    public static void main(String[] args) {
        DataExtractor extractor = new DataExtractor();
        extractor.run();
    }
}


	•	Python Example:

from ViFinanceCrawLib.main import extract_data

data = extract_data("https://finance-news.com")
print(data)



🔥 Removing or Updating the Submodule

❌ Remove the Submodule (if needed)

If you want to remove the submodule and make it a regular directory:

git submodule deinit -f src/main/resources/ViFinanceCrawLib
rm -rf .git/modules/src/main/resources/ViFinanceCrawLib
git rm -f src/main/resources/ViFinanceCrawLib

🔄 Update the Submodule to the Latest Commit

If the submodule has been updated, pull the latest changes:

cd src/main/resources/ViFinanceCrawLib/
git pull origin main
cd ../../../../
git add src/main/resources/ViFinanceCrawLib
git commit -m "Updated submodule to latest commit"
git push origin main



⸻

📝 Contributing
	•	Submit issues and pull requests for improvements.
	•	Keep submodule updates in sync with the main repo.

📄 License

This project is licensed under the MIT License.

