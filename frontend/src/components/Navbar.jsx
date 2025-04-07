import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <nav style={{
      display: "flex",
      justifyContent: "space-around",
      alignItems: "center",
      padding: "1rem",
      backgroundColor: "#f0f0f0",
      borderBottom: "1px solid #ccc"
    }}>
      <Link to="/">Home</Link>
      <Link to="/upload">Upload PDF</Link>
      <Link to="/status">Check PDF Status</Link>
      <Link to="/editor">Editor Login</Link>
      <Link to="/judge">Judge Login</Link>
    </nav>
  );
};

export default Navbar;
