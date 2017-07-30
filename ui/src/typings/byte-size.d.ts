declare module "byte-size" {
    export interface Options {
        precision: number;
        units: 'metric' | 'iec' | 'metric_octet' | 'iec_octet'
    }

    export interface ByteSize {
        value: string;
        unit: string;
        toString(): string;
    }

    export default function byteSize(bytes: number, options?: Options): ByteSize;
}