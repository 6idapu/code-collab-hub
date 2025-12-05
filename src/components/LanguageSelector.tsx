import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import type { Language } from '@/types/interview';

interface LanguageSelectorProps {
  language: Language;
  onChange: (language: Language) => void;
}

const LANGUAGES: { value: Language; label: string }[] = [
  { value: 'javascript', label: 'JavaScript' },
  { value: 'typescript', label: 'TypeScript' },
  { value: 'python', label: 'Python' },
];

export const LanguageSelector = ({ language, onChange }: LanguageSelectorProps) => {
  return (
    <Select value={language} onValueChange={(v) => onChange(v as Language)}>
      <SelectTrigger className="w-36 h-8 text-sm bg-secondary border-border">
        <SelectValue />
      </SelectTrigger>
      <SelectContent>
        {LANGUAGES.map((lang) => (
          <SelectItem key={lang.value} value={lang.value}>
            {lang.label}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
};
