import { toast } from 'react-toastify';

export function successToast(message){
    toast.success(message, {
        position: "top-right",
        autoClose: 2500,
        hideProgressBar: true,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        draggablePercent:30
    });
}

export function infoToast(message){
    toast.info(message, {
        position: "top-right",
        autoClose: 2500,
        hideProgressBar: true,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        draggablePercent:30
    });
}

export function errorToast(message){
    toast.error(message, {
        position: "top-right",
        autoClose: 2500,
        hideProgressBar: true,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        draggablePercent:30
    });
}