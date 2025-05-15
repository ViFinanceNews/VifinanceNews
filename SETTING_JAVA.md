# Java Environment Setup and Project Build Instructions

This guide will help you set up the Java environment for your multi-module Maven project and walk you through the process of building and running the project.

## Prerequisites

Before starting, make sure you have the following tools installed on your machine:

1. **Java Development Kit (JDK) 22**
2. **Apache Maven**
3. **IDE (Optional)**: IntelliJ IDEA, Eclipse, or Visual Studio Code.

### Step 1: Install Java Development Kit (JDK 22)

#### On Windows/macOS/Linux:

1. **Download JDK 22** from the [official Oracle website](https://www.oracle.com/java/technologies/javase/jdk22-archive-downloads.html) or use a package manager:
   - **Windows**: Use the Oracle installer or AdoptOpenJDK.
   - **macOS**: Use Homebrew:
     ```bash
     brew install openjdk@22
     ```
   - **Linux (Ubuntu)**:
     ```bash
     sudo apt install openjdk-22-jdk
     ```

2. Verify the installation:
   ```bash
   java -version

Step 2: Install Apache Maven
	1.	Download Apache Maven from the official website.
	2.	Extract Maven and add the bin directory to your system’s PATH:
	•	Windows: Add the bin folder to the system PATH.
	•	macOS/Linux: Add to the shell profile (~/.bashrc or ~/.zshrc):

export PATH=/path/to/apache-maven/bin:$PATH


	3.	Verify the Maven installation:

mvn -version



Step 3: Clone or Download the Project Repository

Clone the repository or download the project to your local machine:

git clone <repository-url>
cd VifinanceNews

Step 4: Build the Project with Maven
	1.	Navigate to the root directory where the pom.xml file is located.
	2.	Run the following Maven command to build the project:

mvn clean install

This will:
	•	Clean the previous builds.
	•	Download dependencies.
	•	Compile the source code.
	•	Package the project into JAR files.

Step 5: Run the Application

If the main entry point (Main class) is located in com.vifinancenews.Main, you can run the application using:

mvn exec:java -Dexec.mainClass="com.vifinancenews.Main"

Step 6: Set Up Environment Variables (Optional)

If your project uses environment variables (e.g., database URLs, API keys), create a .env file in the root directory:

# .env file example
DB_URL=jdbc:mysql://localhost:3306/mydb
DB_USER=root
DB_PASSWORD=password
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret

You can use the dotenv-java library to load these variables into your application at runtime. Example usage in Java:

Dotenv dotenv = Dotenv.load();
String clientId = dotenv.get("GOOGLE_CLIENT_ID");

Step 7: Running Tests

The project includes unit tests with JUnit 5. To run the tests, use:

mvn test

This will execute the tests across all modules and ensure everything is functioning correctly.

Step 8: IDE Integration (Optional)

For an easier development experience, you can import the project into an IDE:
	•	IntelliJ IDEA: Open the root directory and select “Import Project” -> “Maven”.
	•	Eclipse: Use the Maven plugin to import the project as a Maven project.

This will allow you to build, run, and test your project directly from the IDE.

⸻

Project Structure

Your project is a multi-module Maven setup. Here’s the directory structure:

VifinanceNews/
├── pom.xml               # Parent POM file
├── ViFinanceCommon/      # Common library module
│   └── pom.xml           # Module-specific POM
├── AuthService/          # Authentication service module
│   └── pom.xml           # Module-specific POM
└── UserService/          # User service module
    └── pom.xml           # Module-specific POM

Key Dependencies in AuthService Module
	•	jakarta.mail: For email functionalities.
	•	google-api-client: For OAuth and Google API services.
	•	google-oauth-client: For handling OAuth authentication with Google.

⸻

Troubleshooting
	1.	Java version mismatch: Ensure that JDK 22 is installed and that your pom.xml specifies the correct Java version.
	2.	Missing dependencies: If Maven fails to resolve dependencies, make sure your pom.xml files are correctly configured and your internet connection is stable for downloading from Maven Central.

