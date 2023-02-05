import React from 'react';

import { RxHamburgerMenu } from "react-icons/rx";
import { IoMdClose } from "react-icons/io";
import { Link } from 'react-router-dom';
import {isMobile} from 'react-device-detect';

import './Navbar.css';
import logo from '../images/logo.png'

const Navbar = () => 
{
    const [staticXY, setXY] = React.useState([0, 0]);
    
    function handleMouseMove(e) 
    {
        let xMargin = 0;
        let yMargin = 0;

        let X = e.clientX;
        let Y = e.clientY;
        let specX = window.innerWidth * 1.20;
        let specY = window.innerHeight * 0.60;

        if(specX > X)
        {
            xMargin = (specX - X) / 35;
        }
        else if(specX < X)
        {
            xMargin = (specX - X) / 35;
        }

        if(specY > Y)
        {
            yMargin = (specY - Y) / 40;
        }
        else if(specY < Y)
        {
            yMargin = (specY - Y) / 40;
        }

        setXY([xMargin, -yMargin])
    }

    if(!isMobile)
    {
        window.addEventListener("mousemove", handleMouseMove);
    }


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
            <a href="#">Авторизація</a>
            <span style={isActive && !isMobile ? {marginLeft: staticXY[0], marginBottom: staticXY[1]} : {paddingLeft: "30px", paddingRight: "30px"}}>Борітеся – поборете! Вам Бог помагає! За вас правда, за вас слава і воля святая!</span>
        </div>

        <div id="logotype">
            <img src={logo} alt=""></img>
        </div>
    </>);
};

export default Navbar;