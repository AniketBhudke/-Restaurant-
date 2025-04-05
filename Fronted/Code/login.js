document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
  
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
  
      const email = document.getElementById("email").value.trim();
      const password = document.getElementById("password").value;
  
      const loginData = {
        email: email,
        password: password
      };
  
      try {
        const response = await fetch("http://127.0.0.1:8000/login", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(loginData)
        });
  
        const result = await response.json();
  
        if (response.ok) {
          alert("Login successful!");
          // Redirect to dashboard/home page
          
          window.location.href = "/Fronted/Code/index.html";
        } else {
          alert(result.detail || "Login failed!");
        }
  
      } catch (error) {
        console.error("Login error:", error);
        alert("An error occurred. Please try again later.");
      }
    });
  });
  