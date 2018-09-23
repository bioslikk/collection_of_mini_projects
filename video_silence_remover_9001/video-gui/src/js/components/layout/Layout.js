import React,{Component} from 'react';
import {ToastContainer} from "react-toastify";
import 'react-toastify/dist/ReactToastify.css';
import Board from "./board/Board";

class Layout extends Component{

    render(){
        return(
            <div>
                <Board/>
                <ToastContainer
                    position="bottom-left"
                    autoClose={2500}
                    hideProgressBar
                    newestOnTop={false}
                    closeOnClick
                    rtl={false}
                    pauseOnVisibilityChange
                    draggable
                    pauseOnHover
                />
            </div>
        );
    }
}

export default Layout;