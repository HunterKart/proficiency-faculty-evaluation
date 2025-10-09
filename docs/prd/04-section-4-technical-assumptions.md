### **Section 4: Technical Assumptions**

#### **Repository Structure**

A **Monorepo** is the assumed structure to simplify development and deployment. The Architect must ensure the monorepo has clear internal package boundaries and that the CI/CD pipeline is optimized to build only changed services.

#### **Service Architecture**

The architecture will be a **simple monolith** consisting of a single FastAPI backend API and a single RQ background worker process.

#### **Additional Technical Assumptions**

* **Technology Stack:** The core stack is defined as **React/TypeScript**, **Python/FastAPI**, and **MySQL/MariaDB**.
* **API Style:** The API will be primarily synchronous to maintain simplicity, with asynchronous methods used only where a clear benefit exists.
* **Real-time Functionality:** The system will use a hybrid approach. Real-time updates for job monitoring and notifications will be implemented via WebSockets, while dashboard data refreshes will use frontend polling.
* **AI/ML Models:** All AI models will be run via **local inference**.
* **Deployment Target:** The application will be deployed to a **single VPS (Ubuntu)**, with all services managed via **Docker Compose**.
* **Resource Management:** The Docker configuration must implement resource limits on the worker container to protect system stability.
* **State Management:** Large-scale global state libraries are out of scope. React's **Context API** will be used for minimal global UI state.
* **Disaster Recovery:** The Architect must define a clear disaster recovery plan for the single VPS deployment in the `architecture.md`.

***
