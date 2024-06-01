let isConfigUpdate = false;
let reader = new FileReader();

async function uploadToS3Bucket(stream, extra_details, credential, cd) {
  
    if (!window.AWS) {
      return;
    }
    if (!isConfigUpdate) {
      window.AWS.config.update({ region: credential.region });
      isConfigUpdate = true;
    }

    let s3 = new window.AWS.S3({
      httpOptions: {
        connectTimeout: 5000,
        timeout: 1200000,
      },

      maxRetries: 2,
    //   logger: console,
      retryDelayOptions: {
        customBackoff: (retryCount, err) => {
        //   console.log(`retry: ${retryCount} :: ${err}`);
          extra_details.error_class.text(`retry: ${retryCount} :: ${err}`);
        },
      },
      credentials: new window.AWS.Credentials({
        apiVersion: "latest",
        accessKeyId: credential.accessKeyId,
        secretAccessKey: credential.secretAccessKey,
        signatureVersion: credential.signatureVersion,
        region: credential.region,
        Bucket: credential.Bucket,
      }),
    });

    const fileParams = {
      Bucket: credential.Bucket,
      Key:  "music distribution/song upload/" + extra_details.folder + "/" + extra_details.file.name, // name for the bucket file
      ContentType: extra_details.file.type,
      Body: stream,
    };

    let uploadItem = await s3
      .upload(fileParams, function (err, data) {
        if (err) {
          console.log("Error", err);
          extra_details.error_class.text(err);
        }
        if (data) {
        //   console.log("Upload Success", data.Location);
        }
      })
      .on("httpUploadProgress", function (progress) {
        // console.log("progress=>", progress);
        cd(getUploadingProgress(progress.loaded, progress.total));
      })
      .promise();

    return ({
        status: 1,
        uploadItem: uploadItem,
      });

}

function getUploadingProgress(uploadSize, totalSize) {
  let uploadProgress = (uploadSize / totalSize) * 100;
  return Number(uploadProgress.toFixed(0));
}

async function uploadMedia(file, folder, upload_progress, error_class,AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY) {
  let credentialRequest = {
    accessKeyId: AWS_ACCESS_KEY_ID,
    secretAccessKey: AWS_SECRET_ACCESS_KEY,
    signatureVersion: "v4",
    region: "ap-south-1",
    Bucket: "bluered-production",
  };

  let extra_details = {
    file: file,
    folder: folder,
    error_class: error_class,
    upload_progress: upload_progress,
  };
  let mediaStreamRequest = getFile(extra_details.file);
  const [mediaStream] = await Promise.all([mediaStreamRequest]);
  let result = {status: 0}
  try {
    result = await uploadToS3Bucket(
        mediaStream,
        extra_details,
        credentialRequest,
        (progress) => {
          // console.log(progress);
          extra_details.upload_progress.text(progress + "% uploaded");
        }
      );
    //   console.log(result);
      return result;
  }
  catch(error){
    // console.log(error);
    extra_details.error_class.text(error);
  }

  return result;
}

async function getFile(file) {
  return new Promise((resolve, reject) => {
    let reader = new FileReader();
    reader.onload = (e) => {
      resolve(e.target.result);
    };
    reader.onerror = (err) => {
      reject(false);
    };
    if (file) {
      reader.readAsArrayBuffer(file);
    } else {
     
      extra_details.error_class.text(file);
    }
  });
}
