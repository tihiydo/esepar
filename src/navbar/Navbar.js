import React from 'react';
import './Navbar.css';
import { RxHamburgerMenu } from "react-icons/rx";
import { AiOutlineClose } from "react-icons/ai";

function Navbar() 
{
    const [isActive, setIsActive] = React.useState(false);

    const slideNavbar = () => 
    {
        setIsActive(!isActive);
    };

    return(
    <div>
        <RxHamburgerMenu onClick={slideNavbar} id="openNavBarButton" style={{top: isActive ? "-100px" : "22px"}}/>
        <div id="navbarMain" style={{width: isActive ? "200px" : "0px"}}>
            <AiOutlineClose onClick={slideNavbar} id="closeNavBarButton"/>
            <a href="#">Повітряні тривоги</a>
            <a href="#">Пункти незламності</a>
            <a href="#">єППО</a>
        </div>
    </div>
    );
}

export default Navbar;