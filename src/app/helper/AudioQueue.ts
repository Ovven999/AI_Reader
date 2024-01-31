export class AudioQueue<T> {
    private queue: T[];
    private max_size: number;

    constructor(max_size: number) {
        this.queue = [];
        this.max_size = max_size;
    }

    enqueue(item: T): void {
        if (this.queue.length < this.max_size) {
            this.queue.push(item);
        } else {
            console.log("Queue is full. Cannot enqueue more items.");
        }
    }

    dequeue(): T | undefined {
        if (this.is_empty()) {
            console.log("Queue is empty. Cannot dequeue.");
            return undefined;
        } else {
            return this.queue.shift();
        }
    }

    is_empty(): boolean {
        return this.queue.length === 0;
    }

    is_full(): boolean {
        return this.queue.length === this.max_size;
    }

    size(): number {
        return this.queue.length;
    }

    empty_queue(): void {
        this.queue = [];
    }

    toString(): string {
        return `AudioQueue: ${JSON.stringify(this.queue)}`;
    }
}