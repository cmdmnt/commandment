declare module "byte-size" {

    export = byteSize

    function byteSize(bytes: number, options?: byteSize.Options): byteSize.ByteSize;
    namespace byteSize {
        export interface Options {
            precision: number;
            units: "metric" | "iec" | "metric_octet" | "iec_octet"
        }

        export interface ByteSize {
            value: string;
            unit: string;
            toString(): string;
        }
    }
}
