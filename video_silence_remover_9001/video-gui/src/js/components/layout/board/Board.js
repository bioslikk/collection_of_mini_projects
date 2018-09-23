import React, { Component } from 'react';
import axios from 'axios';
import {API_PATHS} from "../../../api/video/video-api";
import {errorToast, successToast} from "../../../../include/Toasties";
import {Line} from "rc-progress";
import fileDownload from "js-file-download";


export default class Board extends Component {
    constructor(props){
        super(props);
        this.onUpload=this.onUpload.bind(this);
        this.getProgress=this.getProgress.bind(this);
        this.onDownload=this.onDownload.bind(this);
        this.tick=this.tick.bind(this);
        this.getSeconds=this.getSeconds.bind(this);
        this.state={
            isConverted:false,
            conversionFile:'',
            conversionStatus:{},
            uploadProgress:-1,
            elapsed:0,
            start:0
        };

        setInterval(() =>
            {
                if(!this.state.isConverted && this.state.conversionFile !== ''){
                    axios({
                        method:'get',
                        url:API_PATHS.videoStatus(this.state.conversionFile),
                    }).then(
                        (response) => {
                            //console.log(response.data);
                            this.setState({conversionStatus:response.data});
                            if(response.data.stepsCompleted === response.data.totalSteps){
                                this.setState({isConverted:true});
                            }
                        }
                    ).catch((error) => {
                        console.log(error);
                    });
                }
            }
        , 500);
    }

    getSeconds(){
        // Calculate elapsed to tenth of a second:
        let elapsed = Math.round(this.state.elapsed / 100);
        // This will give a number with one digit after the decimal dot (xx.x):
        return (elapsed / 10).toFixed(1);
    }

    tick(){
        if(this.state.start!== 0){
            this.setState({elapsed: new Date() - this.state.start});
        }
        if(this.getProgress() === 100){
            this.setState({start:0});
        }
    }

    componentWillUnmount(){
        clearInterval(this.timer);
    }

    componentDidMount(){
        this.timer = setInterval(this.tick, 50);
    }

    getProgress(){
        if(this.state.conversionStatus.stepsCompleted === undefined || this.state.conversionStatus.totalSteps === undefined){
            return 0
        }
        return this.state.conversionStatus.stepsCompleted / this.state.conversionStatus.totalSteps * 100;
    }

    onUpload(event){
        let data = new FormData();
        data.append('file',event.target.files[0]);
        this.setState({conversionStatus:{}});
        axios({
            method:'post',
            url:API_PATHS.videos(),
            data:data,
            onUploadProgress: (progressEvent) => {
                this.setState({uploadProgress:progressEvent.loaded/progressEvent.total * 100});
            }
        }).then(
            (response) => {
                successToast("Video successfully uploaded, starting conversion");
                this.setState({conversionFile:response.data,isConverted:false, conversionStatus:{}, uploadProgress:-1, elapsed:0,start: new Date()});
            }
        ).catch((error) => {
            console.log(error);
            errorToast('Error in video upload');
        });
        // this line is here because the browser doesn't allow to upload the same file twice without it
        event.target.value='';
    };

    onDownload(){
        axios({
            method:'get',
            url:API_PATHS.videos(this.state.conversionFile),
            responseType: 'blob' // important
        }).then(
            (response) => {
                fileDownload(response.data, this.state.conversionStatus.filename);
            }
        ).catch((error) => {
            if(error.response.status === 404){
                errorToast('File not found');
            }else{
                console.log(error);
            }
        });

    }

    render(){
        let uploadProccess;
        if(this.state.uploadProgress >= 0) {
            uploadProccess = (
                <h5 className="card-title">
                    {this.state.uploadProgress.toFixed(2)}% ...
                </h5>
            );
        }
        // accept=".mpeg, .avi"
        let lineBar=(
            <div style={{paddingBottom:'0.5rem'}}>
                <h5 className="card-title"> Video: {this.state.conversionStatus.filename} </h5>
                <h6> {this.state.conversionStatus.current_state}</h6>
                {uploadProccess}
            </div>
        );
        if(!this.state.isConverted && this.state.conversionFile !== ''){
            lineBar = (
                <div>
                    <h5 className="card-title"> Progress </h5>
                    <h6> {this.state.conversionStatus.current_state}</h6>
                    <Line percent={this.getProgress()} strokeWidth="2" />
                </div>
            );
            if(this.getProgress() === 100){
                lineBar = (
                    <div>
                        <h5 className="card-title"> Completed! </h5>
                        <h6> {this.state.conversionStatus.current_state}</h6>
                        <Line percent={this.getProgress()} strokeWidth="2" strokeColor="#0cd157" />
                    </div>
                );
            }
        }
        let noiseInterval;
        if(this.state.conversionStatus.noises){
            noiseInterval = this.state.conversionStatus.noises.map((noise, index) => {
               return (
                   <div key={index} className="card border-dark mb-3" style={{maxWidth: "150rem",paddingTop:"2px"}}>
                       <div>
                           {noise}
                       </div>
                   </div>
               );
            });
        }
        return (
            <div className="row justify-content-md-center container mx-auto" style={
                {
                    minHeight:'50vh',
                    display:'flex',
                    alignItems:'center'
                }
            }>
                <div className="card border-dark mb-3" style={{maxWidth: "150rem"}}>
                    <div className="card-header">{lineBar}</div>
                    <div className="card-body">
                        <button className="btn btn-block btn-success btn-file" onClick={this.onDownload} disabled={!this.state.isConverted}>
                            <span className="fa fa-download float-left" style={{marginLeft:'1rem'}}/>
                            &nbsp;
                            Download converted video
                        </button>
                        <p className="card-text">
                            <label className="btn btn-block btn-dark btn-file" style={{minWidth:'20rem', marginTop:'1rem'}}>
                                <span className="fa fa-plus float-left" style={{marginLeft:'1rem'}}/>
                                &nbsp;
                                Upload new video <input type="file" style={{display: 'none'}} onChange={this.onUpload}/>
                            </label>
                        </p>
                    </div>
                    Timer: {this.getSeconds()}
                    <br/>
                    A silent moment is only deemed silent if there is no noise in a whole second.
                    {noiseInterval}
                </div>
            </div>
        );
    }
}
