export declare function clean(rut: string): string;
export declare function validate(rut: string): boolean;
export declare function format(rut: string, options?: {
    dots: boolean;
}): string;
export declare function getDigit(rut: string): string | undefined;
