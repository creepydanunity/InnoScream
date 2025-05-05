### **Manual Review for Data Anonymity (User ID Hashing)**

The purpose of this manual review is to ensure that the `user_id` is properly anonymized through hashing, and that the process is compliant with security requirements.

**1. Hashing Functionality:**

* **Implementation**: User IDs are hashed using the SHA-256 algorithm, which converts the original numeric identifier into a hexadecimal string.

* **Code Review**:

  * The `hash_user_id` function receives a `user_id` (int), converts it to a string, encodes it into bytes, and hashes it using `hashlib.sha256()`.

  * A log message is created for the hashing process, capturing only the first few characters of the hash for review purposes.

* **Salting (Global)**:
  A **global salt** has been implemented to further enhance the security of the hashing process. The salt is stored securely in the environment file (`.env`) and is used consistently when hashing all `user_id` values. This salt is combined with the `user_id` before applying the SHA-256 hash function. By using the salt for all users we ensure additional protection against pre-computed attacks (like rainbow tables). The global salt is stored in the `.env` file and loaded securely when needed, ensuring it is not exposed in the code or the database.

* **Audit Logs**: Every hash operation is logged with the part of the `user_id` and the first few characters of the resulting hash for traceability.

**3. Security Considerations:**

* **Hashing Strength**: SHA-256 provides a strong cryptographic hash that is not reversible, ensuring that the original user ID cannot be derived from the hashed value.

**4. Code Integration:**

* **Where It's Used**: The hashed `user_id` is stored in various models, such as `Admin`, `Scream`, `Reaction`, and `UserFeedProgress`.

* **Audit of Models**: Review how the hashed `user_id` is being stored in these models and ensure that it is never stored in its original form (unhashed).

  * **Admin Model**: Stores `user_hash` to represent the admin’s identity.

  * **Scream Model**: Each scream is associated with a `user_hash`, ensuring anonymity of the user who posted the content but still usable to calculate personal statistics.

  * **Reaction Model**: Stores a hashed version of the user’s identity for reactions.

  * **UserFeedProgress Model**: Tracks the hashed `user_id` for personalized feeds, ensuring anonymity when progressing through the feed.

**5. Auditing Process:**

* **Bandit Review**: Utilized Bandit to scan the codebase for potential vulnerabilities related to user data handling. None found.

* **Manual Review**:

  * Inspected each instance of the `user_id` being hashed in the models to ensure there are no direct exposures.

  * Confirmed that only the hashed value is stored and processed across the application.

**6. Validation:**

* Performed a manual check by querying the database and ensuring that:

  * User IDs are consistently stored as hashes and not as plain text.

  * The system does not inadvertently expose raw user IDs in logs or error messages.
