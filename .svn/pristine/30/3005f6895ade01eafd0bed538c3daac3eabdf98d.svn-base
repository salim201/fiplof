ALTER TABLE public.contribuable RENAME "CIN"  TO cin;
ALTER TABLE public.contribuable
ADD COLUMN sexe character varying(50);
ALTER TABLE public.contribuable
ADD COLUMN idcontribuableconsorts bigint;
ALTER TABLE public.contribuable
  ADD CONSTRAINT fk_consort FOREIGN KEY (idcontribuableconsorts) REFERENCES public.contribuable (idcontribuable)
   ON UPDATE NO ACTION ON DELETE NO ACTION;
CREATE INDEX fki_consort
  ON public.contribuable(idcontribuableconsorts);
  
ALTER TABLE public.contribuable
   ADD COLUMN lieucin character varying(80);