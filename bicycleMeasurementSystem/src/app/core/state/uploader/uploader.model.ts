export interface Uploader {
  id?: number;
  pixelRatio?: number;
  imgWidth?: number;
  imgHeight?: number;
  saddleHeight?: number;
  Reach?: number;
  list?: any;
}

export function createUploader(params: Partial<Uploader>) {
  return {

  } as Uploader;
}
