export const BASE_API = "http://localhost:4001/v1";

export const API_PATHS = {
        videos: (id) => {
            if (id) {
                return BASE_API + "/videos/" + id;
            }
            return BASE_API + "/videos";
        },
        videoStatus: (id) => BASE_API + "/videos/" + id+"/status"
};