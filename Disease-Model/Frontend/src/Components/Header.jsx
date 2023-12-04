import React from 'react'
import { Link } from "react-router-dom";
import "./header.css"

const Header = () => {
  return (
    <div className='header'>
      <div className='header-logo'>
      <img src='/logo.png' alt='logo' />
      </div>
      <div className='titleBar'>
        <Link className="titleBarHeading" to={"/"}>Home</Link>
        <Link className="titleBarHeading" to={"/search"}>Search </Link>
        <Link className="titleBarHeading" to={"/about"}>About </Link>
        <Link className="titleBarHeading" to={"/login"}>Profile</Link>
      </div>
    </div>
  )
}

export default Header