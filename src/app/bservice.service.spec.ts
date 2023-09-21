import { TestBed } from '@angular/core/testing';

import { BserviceService } from './bservice.service';

describe('BserviceService', () => {
  let service: BserviceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(BserviceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
