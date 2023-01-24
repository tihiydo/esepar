import React from 'react';
import './Navbar.css';

import { RxHamburgerMenu } from "react-icons/rx";
import { IoMdClose } from "react-icons/io";
import { Link } from 'react-router-dom';

const Navbar = () => 
{
    const [isActive, setIsActive] = React.useState(false);

    const slideNavbar = () => 
    {
        setIsActive(!isActive);
    };

    return(
    <>
        <RxHamburgerMenu onClick={slideNavbar} id="openNavBarButton" style={isActive ? {top: "-100px", opacity : 0} : {top: "22px", opacity : 1.0}}/>
        <div id="navbarMain" style={{left: isActive ? "0px" : "-240px"}}>
            <IoMdClose onClick={slideNavbar} id="closeNavBarButton"/>
            <Link to="/alerts">Повітряні тривоги</Link>
            <Link to="/invincibility">Пункти незламності</Link>
            <a href="#">Скоро</a>
        </div>
    </>);
};

export { Navbar };